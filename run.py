import logging.handlers
import os
from logging.config import dictConfig

import yaml

from categorizer.categorizer import Categorizer
from categorizer.iris_helper import IrisHelper
from settings import config_by_name

app_settings = config_by_name[os.getenv('sysenv', 'dev')]()

path = ''
value = os.getenv('LOG_CFG')
if value:
    path = value
if os.path.exists(path):
    with open(path, 'rt') as f:
        lconfig = yaml.safe_load(f.read())
    dictConfig(lconfig)
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    c = Categorizer(app_settings)
    i = IrisHelper(app_settings)

    incidents = {}

    logger.info('Pulling incidents...')
    incident_list = i.data_pull()
    for incident in incident_list:
        incidents[str(incident[0])] = incident[1]

    logger.info('Starting Garbage run...')
    incidents = c.cleanup(incidents)

    logger.info('Starting Leo Move...')
    incidents = c.leomove(incidents)

    logger.info('Starting categorize...')
    c.categorize(incidents)

    logger.info('All Abuse@ functions complete')
