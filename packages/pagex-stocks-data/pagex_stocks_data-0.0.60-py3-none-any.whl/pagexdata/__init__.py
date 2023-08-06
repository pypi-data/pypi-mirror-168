import logging
import sys

# setup logger
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("{asctime} {levelname}: {message}", "%d.%m.%Y %H:%M:%S", style="{")
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel("INFO")

logger.info("Called package pagexdata")
