from categorizer.categorizer import Categorizer
import logging.config
import os
import yaml

# setup logging
path = 'logging.yml'
value = os.getenv('LOG_CFG', None)
if value:
    path = value
if os.path.exists(path):
    with open(path, 'rt') as f:
        lconfig = yaml.safe_load(f.read())
    logging.config.dictConfig(lconfig)
else:
    logging.basicConfig(level=logging.INFO)


_logger = logging.getLogger(__name__)

c = Categorizer()

logging.info('Starting Garbage run...')
c.cleanup()

logging.info('Starting Leo Move...')
c.leomove()

logging.info('Starting categorize...')
c.categorize()

logging.info('All Abuse@ functions complete')
