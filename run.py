from categorizer.categorizer import Categorizer
import logging

c = Categorizer()

logging.info('Starting Garbage run...')
c.cleanup()

logging.info('Starting Leo Move...')
c.leomove()

logging.info('Starting categorize...')
c.categorize()

logging.info('All Abuse@ functions complete')
