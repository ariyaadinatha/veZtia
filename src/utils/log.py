# used to setup to get log info and error
import logging
import os


isDirectoryLogExists = os.path.isdir('log')

directory = "log"

# Create directory if not exists
if not os.path.exists(directory):
    os.makedirs(directory)

logging.basicConfig(filename='log/veztia.log',
    format='[%(asctime)s-%(levelname)s-%(funcName)s-%(lineno)d]: %(message)s', level=logging.INFO)

logger = logging.getLogger("veztia")