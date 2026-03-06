import logging
import os

# membuat folder logs jika belum ada
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_error(error_message):
    logging.error(error_message)