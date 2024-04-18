# Scrapper class for https://www.argentina.gob.ar/normativa/
#
# Example usage:
# from scrapper import Scrapper
# scrapper = Scrapper()
# data = scrapper('2023-12-11')

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Scrapper:
    def __init__(self, max_retries: int = 5, retry_sleep: int = 10) -> None:
        self.max_retries = max_retries
        self.retry_sleep = retry_sleep
        logging.info("Scrapper initialized with max_retries=%s and retry_sleep=%s", max_retries, retry_sleep)

    def fetch_urls_for_date(self, date: datetime) -> List[Dict[str, str]]:
        formatted_date = date.strftime("%Y-%m-%d")
        urls = []
        pagina = 1
        params = {
            'jurisdiccion': 'nacional',
            'tipo_norma': 'legislaciones',
            'publicacion_desde': formatted_date,
            'publicacion_hasta': formatted_date,
            'limit': '50',
            'offset': pagina,
        }
        logging.info("Fetching URLs for date: %s", formatted_date)

        while True:
            response = requests.get('https://www.argentina.gob.ar/normativa/busqueda-avanzada', params=params)
            if response.status_code != 200:
                logging.warning("Failed to fetch data with status code: %s", response.status_code)
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            rows = soup.find_all('tr', class_='panel')
            if not rows:
                logging.info("No more rows found, ending URL fetch.")
                break

            for row in rows:
                numero_cell = row.find('td', class_='numero')
                descripcion_cell = row.find('td', class_='descripcion')
                if numero_cell and descripcion_cell:
                    link_tag = numero_cell.find('a')
                    if link_tag and 'href' in link_tag.attrs:
                        urls.append({
                            'url': f"https://www.argentina.gob.ar{link_tag['href']}",
                            'fecha': formatted_date,
                            'descripcion': descripcion_cell.text.strip()
                        })
            pagina += 1
            params['offset'] = pagina

        logging.info("Total URLs fetched: %s", len(urls))
        return urls

    def fetch_content(self, entry: Dict[str, str]) -> Optional[Dict[str, str]]:
        logging.info("Fetching content for URL: %s", entry['url'])
        for attempt in range(self.max_retries):
            try:
                response = requests.get(entry['url'])
                if response.status_code != 200:
                    logging.warning("Failed to fetch content for URL: %s with status code: %s", entry['url'], response.status_code)
                    return None

                soup = BeautifulSoup(response.content, 'html.parser')
                entity = soup.find('p', class_='lead m-b-0').find('small').text.strip() if soup.find('p', class_='lead m-b-0') and soup.find('p', class_='lead m-b-0').find('small') else ''
                title = soup.find('h2', class_='h5').text.strip() if soup.find('h2', class_='h5') else ''
                name = soup.find('h1', class_='h5').text.strip() if soup.find('h1', class_='h5') else ''
                summary = soup.find('article').text.strip() if soup.find('article') else ''

                content_links = [a['href'] for a in soup.find_all('a', href=True) if '/actualizacion' in a['href'] or '/texto' in a['href']]
                chosen_link = next((link for link in content_links if '/actualizacion' in link), content_links[0] if content_links else None)
                urls_in_article = []

                full_text = ''
                if chosen_link:
                    chosen_response = requests.get(f"https://www.argentina.gob.ar{chosen_link}")
                    if chosen_response.status_code == 200:
                        chosen_soup = BeautifulSoup(chosen_response.content, 'html.parser')
                        article = chosen_soup.find('article')
                        if article:
                            urls_in_article = [a['href'] for a in article.find_all('a', href=True)]
                            full_text = article.text.strip()
                        else:
                            full_text = ''
                else:
                    full_text = summary  # Use summary if no specific URL was found or navigated to.

                return {'title': title, 'name': name, 'entity': entity, 'summary': summary, 'full_text': full_text, 'url_in_articles':urls_in_article, 'date': entry['fecha'], 'url': entry['url'].split('argentina.gob.ar')[1]}
            except requests.exceptions.Timeout:
                logging.warning("Timeout occurred for URL: %s (Attempt %s/%s)", entry['url'], attempt + 1, self.max_retries)
                if attempt + 1 == self.max_retries:
                    logging.error("Max retries reached for URL: %s", entry['url'])
                    break
                time.sleep(self.retry_sleep)
            except requests.exceptions.RequestException as e:
                logging.error("Request exception for URL: %s: %s", entry['url'], str(e))
                break
        return None

    def __call__(self, date_str: str, max_workers: int = 5) -> List[Dict[str, str]]:
        """
        Call method to scrape data for a given date.

        Args:
        date_str: The date in 'YYYY-MM-DD' format.
        max_workers: (optional) The maximum number of worker threads for the ThreadPoolExecutor. Default is 5.

        Returns:
        A list of dictionaries containing scraped data in the format {'title','name','entity','content','date'}.
        """
        date = datetime.strptime(date_str, '%Y-%m-%d')
        urls = self.fetch_urls_for_date(date)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(self.fetch_content, url): url for url in urls}
            results = [future.result() for future in as_completed(future_to_url)]
        
        return [result for result in results if result]