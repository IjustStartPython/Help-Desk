
import logging
from pathlib import Path
import os
import sys
from datetime import datetime

def setup_logger():
    if sys.platform == "win32":
        base_path = Path(os.environ.get('APPDATA', os.path.expanduser('~')))
    else:
        base_path = Path.home() / '.local' / 'share'

    log_folder = base_path / 'Help-Desk' / 'logs'
    log_folder.mkdir(parents=True, exist_ok=True)

    log_file = log_folder / f"helpdesk_{datetime.now().strftime('%Y%m%d')}.log"

    logger = logging.getLogger('HelpDesk')
    logger.setLevel(logging.INFO)

    # Éviter d'ajouter plusieurs handlers si déjà configuré________________________
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Logger global______________________________________________________________________
logger = setup_logger()
