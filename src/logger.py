from loguru import logger


logger.add("../logs/log.log", level="INFO", rotation="10 MB")
