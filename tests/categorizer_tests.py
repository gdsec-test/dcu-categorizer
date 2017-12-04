from nose.tools import assert_equal
from mock import patch
from categorizer.categorizer import Categorizer
from categorizer.categorizer import IrisHelper

import logging.handlers


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
        incidents = {'123456': 'testing@sh.baidu.com',
                     '987654': 'testing@testing.com',
                     '456789': 'testing@peakindustry.com'}

        results = self._cat.cleanup(incidents)

        expected = {'987654': 'testing@testing.com'}

        return assert_equal(results, expected)

    def test_leomove(self):
        pass
        incidents = {'1355224': 'testing@rkn.gov.ru',
                     '1355225': 'testing@testing.com'}

        results = self._cat.leomove(incidents)

        expected = {'1355225': 'testing@testing.com'}

        return assert_equal(results, expected)

    @patch.object(IrisHelper, 'note_puller')
    @patch.object(Categorizer, '_move')
    def test_categorizer(self, _move, note_puller):

        incidents = {'1355218': 'testing@testing'}

        results = self._cat.categorize(incidents)

        note_puller.return_value = {'1355218': ('no body phishing test', 'asdfaefefawef')}

        expected = {'malware': [], 'spam': [], 'phishing': ['1355218'], 'close': [], 'netabuse': [],
                    'left': []}

        return assert_equal(results, expected)
