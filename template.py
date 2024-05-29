import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]:%(message)s:')

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prmopt.py",
    ".env",
    "setup.py",
    "app.py",
    "store_index.py",
    "static/.gitkeep",
    "tempelates/chat.html",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    
    if filedir != "":
        if not os.path.exists(filedir):
            os.makedirs(filedir, exist_ok=True)
            logging.info(f"Created directory {filedir} for the file {filename}")
        elif not os.path.isdir(filedir):
            logging.error(f"Cannot create directory {filedir}, a file with the same name exists")
            continue
        else:
            logging.info(f"Directory {filedir} already exists")
    
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file {filename}")
    else:
        logging.info(f"{filename} is already created")
