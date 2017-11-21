from mock import patch
from nose.tools import assert_equal

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


class TestCategorizer:

    def __init__(self):
        self._cat = Categorizer(_logger)

    @patch.object(IrisHelper, 'data_pull')
    @patch.object(IrisHelper, 'ticket_move')
    @patch.object(IrisHelper, 'ticket_close')
    @patch.object(IrisHelper, 'ticket_update')
    def test_categorizer(self, ticket_update, ticket_close, ticket_move, data_pull):
        data_pull.return_value = {1354877: ('Paddy Test', 'another test'),
                                  1354888: ('TIME-SENSITIVE - PHISHING / Incident ID: 28125353 / '
                                             'IP Address: 23.229.236.134 / ASN: AS-26496-GO-DADDY-COM-LLC - '
                                             'GoDaddy.com, LLC, US',
                                             'TIME-SENSITIVE - PHISHING / Incident ID: 28126012'
                                             ' / IP Address: 192.169.197.43 / ASN: AS-26496-GO-DADDY-COM-LLC - '
                                             'GoDaddy.com, LLC, US'),
                                  1354768: ('Televisa: AV infringement - TelevisaCaseID-11566254',
                                             'SSH brute-force from your network / domain (184.168.200.238)'),
                                  1359823: ('bad guy alert', 'I got a virus!!!! 123.123.123.123'),
                                  1356874: ('things and stuff',
                                             'Spam-Distributed Counterfeit Goods Spam Incident Report 1400806'),
                                  1357985: ('trademark stolen!!', 'some stuff')}

        result = self._cat.categorize()
        expected = {'malware': [1359823], 'spam': [1356874], 'phishing': [1354888], 'close': [1357985],
                    'netabuse': [1354768], 'left': {1354877: ('Paddy Test', 'another test')}}
        assert_equal(result, expected)
