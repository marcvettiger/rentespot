import logging
import logging.config

logging.config.fileConfig('../cfg/logger.conf')
logger = logging.getLogger()
