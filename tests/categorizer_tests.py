from nose.tools import assert_equal
from mock import patch
from categorizer.categorizer import Categorizer
from categorizer.categorizer import IrisHelper
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

        return assert_equal(results, expected)

    def test_leomove(self):
        """
        recommended to create dev IRIS tickets and use IIDs and emails in test
        :return:
        """
        incidents = {'1355224': 'testing@rkn.gov.ru',
                     '1355225': 'testing@testing.com'}

        results = self._cat.leomove(incidents)

        expected = {'1355225': 'testing@testing.com'}

        return assert_equal(results, expected)

    def test_categorizer(self):
        """
        IRIS tickets created in dev IRIS and IIDs and from email
        :return:
        """
        incidents = {'1355218': 'testing@testing',
                     '1355212': 'garbage@testing.com'}

        results = self._cat.categorize(incidents)

        expected = {'malware': [], 'spam': [], 'phishing': ['1355218'], 'close': ['1355212'], 'netabuse': [],
                    'left': []}

        return assert_equal(results, expected)
