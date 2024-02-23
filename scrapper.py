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

class Scrapper:
    def __init__(self, max_retries: int = 5, retry_sleep: int = 10) -> None:
        """
        Initialize the Scrapper class with optional max retries and retry sleep parameters.

        Args:
        max_retries: (optional) Maximum number of retries for HTTP requests.
        retry_sleep: (optional) Seconds to wait between retries.
        """
        self.max_retries = max_retries
        self.retry_sleep = retry_sleep

    def fetch_urls_for_date(self, date: datetime) -> List[Dict[str, str]]:
        """
        Fetch URLs for a given date from the specified website.

        Args:
        date: The date for which to fetch URLs.
        
        Returns:
        A list of dictionaries, each containing URL and related data.
        """
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

        while True:
            response = requests.get(
                'https://www.argentina.gob.ar/normativa/busqueda-avanzada',
                params=params,
            )
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            rows = soup.find_all('tr', class_='panel')
            if not rows:
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

        return urls

    def fetch_content(self, entry: Dict[str, str]) -> Optional[Dict[str, str]]:
        """
        Fetch content for a given entry (URL and related data).

        Args:
        entry: A dictionary containing URL and related data.

        Returns:
        A dictionary with fetched content or None if an error occurs.
        """
        for attempt in range(self.max_retries):
            try:
                url = entry['url']
                response = requests.get(url)
                if response.status_code != 200:
                    return None

                soup = BeautifulSoup(response.content, 'html.parser')
                entity = soup.find('p', class_='lead m-b-0').find('small').text.strip() if soup.find('p', class_='lead m-b-0') and soup.find('p', class_='lead m-b-0').find('small') else ''
                title = soup.find('h2', class_='h5').text.strip() if soup.find('h2', class_='h5') else ''
                name = soup.find('h1', class_='h5').text.strip() if soup.find('h1', class_='h5') else ''

                content_link = soup.find('a', class_='btn btn-link')
                content_url = f"https://www.argentina.gob.ar{content_link['href']}" if content_link and 'href' in content_link.attrs else ''

                content = ''
                if content_url:
                    content_response = requests.get(content_url)
                    if content_response.status_code == 200:
                        content_soup = BeautifulSoup(content_response.content, 'html.parser')
                        content_article = content_soup.find('article')
                        content = content_article.text.strip() if content_article else ''
                else:
                    content = soup.find('article').text.strip()
                date = entry['fecha']

                return {'title': title, 'name': name, 'entity': entity, 'content': content, 'date': date, 'url':url.split('argentina.gob.ar')[1]}
            except requests.exceptions.Timeout:
                if attempt + 1 == self.max_retries:
                    break
                time.sleep(self.retry_sleep)
            except requests.exceptions.RequestException:
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
