from categorizer.categorizer import Categorizer
import logging
import logging.handlers

# SET UP LOGGING

logging.basicConfig(filename='categorizer.log', level=logging.INFO,
                    format="[%(levelname)s:%(asctime)s:%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
                    )
log_handler = logging.handlers.RotatingFileHandler(filename='categorizer.log', backupCount=5, maxBytes=5 * 1024 * 1024)
_logger = logging.getLogger(__name__)
_logger.addHandler(log_handler)

c = Categorizer()

_logger.info('Starting Garbage run...')
c.cleanup()

#_logger.info('Starting Leo Move...')
#c.leomove()

_logger.info('Starting categorize...')
c.categorize()

_logger.info('All Abuse@ functions complete')
