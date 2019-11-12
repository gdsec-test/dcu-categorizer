from nose.tools import assert_equal

from categorizer.categorizer import Categorizer
from settings import config_by_name


class TestCategorizer:

    def __init__(self):
        self._cat = Categorizer(config_by_name['test']())

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
