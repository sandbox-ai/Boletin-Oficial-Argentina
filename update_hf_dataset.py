import os
import subprocess
from dataset_utils import update
from scrapper import Scrapper

# Configuration
HF_USER = os.getenv('HF_USER')
HF_DATASET = os.getenv('HF_DATASET')
REPO_PATH = f"{HF_USER}/{HF_DATASET}"
DATASET_FILE = 'boletin-oficial-argentina.jsonl'

# Clone the dataset repository
subprocess.run(['git', 'clone', f'https://huggingface.co/datasets/{REPO_PATH}', 'HF_DATASET'], check=True)

# Update the dataset
scrapper = Scrapper()
update(scrapper, DATASET_FILE)

# Add and commit changes
#subprocess.run(['git', 'add', DATASET_FILE], check=True)
#subprocess.run(['git', 'commit', '-m', 'Update dataset'], check=True)
# Commented because pushing is handled by the GitHub Action itself.
