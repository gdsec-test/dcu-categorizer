from nose.tools import assert_equal
import run

import logging.handlers


# SET UP LOGGING

log_handler = logging.handlers.RotatingFileHandler(filename='categorizer.log', backupCount=5, maxBytes=5 * 1024 * 1024)
formatter = logging.Formatter("[%(levelname)s:%(asctime)s:%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")
log_handler.setFormatter(formatter)
_logger = logging.getLogger(__name__)
_logger.addHandler(log_handler)
_logger.setLevel(logging.INFO)


class TestCategorizer:

    def test_categorizer(self):
        """
        Create IRIS tickets in dev-iris.
        Insert IIDs as strings in expected dictionary.
        Test may show ERROR due to Suds
        Last coverage: 92%
        :return:
        """

        result = run
        expected = {'malware': ['1355210'], 'spam': ['1355211'], 'phishing': ['1355208'], 'close': ['1355212'],
                    'netabuse': ['1355209'], 'left': ['1355207']}
        assert_equal(result, expected)
