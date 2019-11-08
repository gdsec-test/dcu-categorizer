from nose.tools import assert_equal
from categorizer.categorizer import Categorizer
import logging.handlers

"""
Recommended settings for testing:
--with-coverage --cover-package=categorizer --cover-html --cover-erase --nologcapture
nologcapture avoids suds log dumps into the testing
"""


# SET UP LOGGING

log_handler = logging.handlers.RotatingFileHandler(filename='categorizer.log', backupCount=5, maxBytes=5 * 1024 * 1024)
formatter = logging.Formatter("[%(levelname)s:%(asctime)s:%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")
log_handler.setFormatter(formatter)
_logger = logging.getLogger(__name__)
_logger.addHandler(log_handler)
_logger.setLevel(logging.INFO)


class TestCategorizer:

    def __init__(self):
        self._cat = Categorizer(_logger)

    def test_cleanup(self):
        """
        recommended to create dev IRIS tickets and use IIDs and emails in test
        :return:
        """
        incidents = {'123456': 'testing@sh.baidu.com',
                     '987654': 'testing@testing.com',
                     '456789': 'testing@peakindustry.com'}

        results = self._cat.cleanup(incidents)

        expected = {'987654': 'testing@testing.com'}

        assert_equal(results, expected)
