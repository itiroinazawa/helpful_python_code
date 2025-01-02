import logging

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger("API")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("API started")
