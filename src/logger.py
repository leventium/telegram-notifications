import os
import sys
from pathlib import Path
from loguru import logger


LOG_PATH = Path(__file__).parent.parent.joinpath("logs").joinpath("info.log")
LOG_LEVEL = "DEBUG" if "DEBUG" in os.environ else "INFO"


logger.add(str(LOG_PATH), level=LOG_LEVEL, rotation="10 MB")
