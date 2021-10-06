"""
This is a logger module for cep_finder api
"""
import logging
import os

log_level = logging.DEBUG

if os.getenv('LOG_LEVEL') == "DEBUG":
    log_level = logging.DEBUG
elif os.getenv('LOG_LEVEL') == "INFO":
    log_level = logging.INFO
elif os.getenv('LOG_LEVEL') == "WARNING":
    log_level = logging.WARNING
elif os.getenv('LOG_LEVEL') == "ERROR":
    log_level = logging.ERROR
elif os.getenv('LOG_LEVEL') == "CRITICAL":
    log_level = logging.CRITICAL


logger = logging.getLogger(__name__)
logger.setLevel(log_level)

handler = logging.StreamHandler()
handler.setLevel(log_level)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
