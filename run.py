from categorizer.categorizer import Categorizer
import logging

# SET UP LOGGING
logging.basicConfig(filename='categorizer.log', level=logging.INFO,
                    format="[%(levelname)s:%(asctime)s:%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
                    )
_logger = logging.getLogger(__name__)

c = Categorizer()

_logger.info('Starting Garbage run...')
c.cleanup()

_logger.info('Starting Leo Move...')
c.leomove()

_logger.info('Starting categorize...')
c.categorize()

_logger.info('All Abuse@ functions complete')
