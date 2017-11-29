from categorizer.categorizer import Categorizer
from categorizer.iris_helper import IrisHelper
import logging.handlers

# SET UP LOGGING

log_handler = logging.handlers.RotatingFileHandler(filename='categorizer.log', backupCount=5, maxBytes=5 * 1024 * 1024)
formatter = logging.Formatter("[%(levelname)s:%(asctime)s:%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")
log_handler.setFormatter(formatter)
_logger = logging.getLogger(__name__)
_logger.addHandler(log_handler)
_logger.setLevel(logging.INFO)

c = Categorizer(_logger)
i = IrisHelper(_logger)

incidents = {}

_logger.info('Pulling incidents...')
incident_list = i.data_pull()
for incident in incident_list:
    incidents[str(incident[0])] = incident[1]


_logger.info('Starting Garbage run...')
incidents = c.cleanup(incidents)

_logger.info('Starting Leo Move...')
incidents = c.leomove(incidents)

_logger.info('Starting categorize...')
c.categorize(incidents)

_logger.info('All Abuse@ functions complete')
