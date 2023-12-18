# Utils to create and update dataset by 
# scrapping https://www.argentina.gob.ar/normativa/

import json
import logging
from datetime import datetime, timedelta
from typing import Callable, List, Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update(scrapper: Callable[[str], List[Dict]], file_path: str) -> None:
    """
    Update the dataset by scraping new data since the last recorded date in the JSONL file.
    
    Args:
    scrapper: Our scrapper object for Boletín Oficial.
    file_path: Path to the JSONL file where the data is stored.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            last_line = list(file)[-1]
            last_data = json.loads(last_line)
            last_date = datetime.strptime(last_data['date'], '%Y-%m-%d')
    except (FileNotFoundError, IndexError, json.JSONDecodeError) as e:
        logging.error(f"Error reading file: {e}")
        last_date = datetime.now() - timedelta(days=1)

    next_date = last_date + timedelta(days=1)
    current_date = datetime.now()

    while next_date <= current_date:
        logging.info(f"Scraping data for {next_date.strftime('%Y-%m-%d')}")
        daily_data = scrapper(next_date.strftime('%Y-%m-%d'))
        if daily_data:
            with open(file_path, 'a', encoding='utf-8') as file:
                for data in daily_data:
                    file.write(json.dumps(data, ensure_ascii=False) + '\n')
        else:
            logging.warning(f"No data found for {next_date.strftime('%Y-%m-%d')}")
        next_date += timedelta(days=1)
    logging.info("Update complete.")

def create(scrapper: Callable[[str], List[Dict]], file_path: str, start_date: str = '1893-07-01') -> None:
    """
    Create a new dataset by scraping data starting from the given date up to the current date.
    
    Args:
    scrapper: Our scrapper object for Boletín Oficial.
    file_path: Path to the JSONL file where the data will be stored.
    start_date: (optional) The start date for data scraping in 'YYYY-MM-DD' format.
    """
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    current_date = datetime.now()

    with open(file_path, 'w', encoding='utf-8') as file:
        while start_date <= current_date:
            logging.info(f"Scraping data for {start_date.strftime('%Y-%m-%d')}")
            daily_data = scrapper(start_date.strftime('%Y-%m-%d'))
            if daily_data:
                for data in daily_data:
                    file.write(json.dumps(data, ensure_ascii=False) + '\n')
            else:
                logging.warning(f"No data found for {start_date.strftime('%Y-%m-%d')}")
            start_date += timedelta(days=1)
    logging.info("Dataset creation complete.")
