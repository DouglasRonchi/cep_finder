import os
import unittest
from unittest.mock import patch


class MyTestCase(unittest.TestCase):
    def test_logger(self):
        with patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"}):
            from app.utils.logger import logger
            logger.debug("DEBUG")
            logger.info("INFO")
            logger.warning("WARNING")
            logger.error("ERROR")
            logger.critical("CRITICAL")

    def test_logger_info(self):
        with patch.dict(os.environ, {"LOG_LEVEL": "INFO"}):
            from app.utils.logger import logger
            logger.debug("DEBUG")
            logger.info("INFO")
            logger.warning("WARNING")
            logger.error("ERROR")
            logger.critical("CRITICAL")

    def test_logger_warning(self):
        with patch.dict(os.environ, {"LOG_LEVEL": "WARNING"}):
            from app.utils.logger import logger
            logger.debug("DEBUG")
            logger.info("INFO")
            logger.warning("WARNING")
            logger.error("ERROR")
            logger.critical("CRITICAL")

    def test_logger_error(self):
        with patch.dict(os.environ, {"LOG_LEVEL": "ERROR"}):
            from app.utils.logger import logger
            logger.debug("DEBUG")
            logger.info("INFO")
            logger.warning("WARNING")
            logger.error("ERROR")
            logger.critical("CRITICAL")

    def test_logger_critical(self):
        with patch.dict(os.environ, {"LOG_LEVEL": "CRITICAL"}):
            from app.utils.logger import logger
            logger.debug("DEBUG")
            logger.info("INFO")
            logger.warning("WARNING")
            logger.error("ERROR")
            logger.critical("CRITICAL")


if __name__ == '__main__':
    unittest.main()
