import os
import subprocess
from dataset_utils import update
from scrapper import Scrapper

# Configuration
DATASET_FILE = 'boletin-oficial-argentina.jsonl'

# Update the dataset
scrapper = Scrapper()
update(scrapper, DATASET_FILE)