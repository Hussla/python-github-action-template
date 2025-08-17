import logging
import logging.handlers
import os

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")

    try:
        r = requests.get('https://weather.talkpython.fm/api/weather/?city=Berlin&country=DE')
        if r.status_code == 200:
            data = r.json()
            temperature = data["forecast"]["temp"]
            logger.info(f'Weather in Berlin: {temperature}')
        elif r.status_code == 429:
            logger.warning(f'API rate limit exceeded (status code: {r.status_code}). This is temporary and will reset automatically.')
            logger.warning(f'Error message: {r.text}')
            logger.info('Next run will occur in 1 hour due to updated schedule.')
        else:
            logger.error(f'API request failed with status code: {r.status_code}')
            logger.error(f'Error message: {r.text}')
    except Exception as e:
        logger.error(f'Exception occurred during API request: {e}')
