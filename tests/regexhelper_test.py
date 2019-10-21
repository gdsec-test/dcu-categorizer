from nose.tools import assert_equal
from categorizer.regex_helper import ListHelper
import categorizer.listings as lst


class TestRegexHelper:

    def __init__(self):
        self._reg = ListHelper()

    def test_csam_summary(self):
        incident = {'123456': ('CSAM report', 'bad stuff.'), '654321': ('phishing report', 'bad stuff')}
        results = self._reg.reg_logic(incident, lst.csam_keys)
        expected = (['123456'], {'654321': ('phishing report', 'bad stuff')})

        return assert_equal(results, expected)

    def test_phish_summary(self):
        incident = {'123456': ('fake login', 'bad stuff.'), '654321': ('csam report', 'bad stuff')}
        results = self._reg.reg_logic(incident, lst.phish_keys)
        expected = (['123456'], {'654321': ('csam report', 'bad stuff')})

        return assert_equal(results, expected)

    def test_mal_summary(self):
        incident = {'123456': ('website gave me a virus', 'bad stuff.'), '654321': ('phishing report', 'bad stuff')}
        results = self._reg.reg_logic(incident, lst.malware_keys)
        expected = (['123456'], {'654321': ('phishing report', 'bad stuff')})

        return assert_equal(results, expected)

    def test_net_summary(self):
        incident = {'123456': ('Botnet command and control', 'bad stuff.'), '654321': ('phishing report', 'bad stuff')}
        results = self._reg.reg_logic(incident, lst.netabuse_keys)
        expected = (['123456'], {'654321': ('phishing report', 'bad stuff')})

        return assert_equal(results, expected)

    def test_csam_body(self):
        incident = {'123456': ('bad things', 'found some phishing but actually its child abuse.'), '654321': ('bad things', 'Found lots of phishing')}
        results = self._reg.reg_logic(incident, lst.csam_keys)
        expected = (['123456'], {'654321': ('bad things', 'Found lots of phishing')})

        return assert_equal(results, expected)

    def test_phish_body(self):
        incident = {'123456': ('bad things', 'found some phishing but actually its child abuse.'), '654321': ('bad things', 'Found lots of viruses')}
        results = self._reg.reg_logic(incident, lst.phish_keys)
        expected = (['123456'], {'654321': ('bad things', 'Found lots of viruses')})

        return assert_equal(results, expected)

    def test_mal_body(self):
        incident = {'123456': ('bad things', 'found some phishing but actually its a trojan.'), '654321': ('bad things', 'Found lots of phishing')}
        results = self._reg.reg_logic(incident, lst.malware_keys)
        expected = (['123456'], {'654321': ('bad things', 'Found lots of phishing')})

        return assert_equal(results, expected)

    def test_net_body(self):
        incident = {'123456': ('bad things', 'found some attempted login failures, check the logs.'), '654321': ('bad things', 'Found lots of phishing')}
        results = self._reg.reg_logic(incident, lst.netabuse_keys)
        expected = (['123456'], {'654321': ('bad things', 'Found lots of phishing')})

        return assert_equal(results, expected)
