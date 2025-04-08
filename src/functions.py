from datetime import datetime
from pathlib import Path

DIR_PATH = Path(__name__).parent
NOW = str(datetime.now())[:19]


def save_log(error: str):
    with open(DIR_PATH / '.log', 'a') as log_file:
        log_file.write(f'-{NOW}\n---{error}\n\n')
