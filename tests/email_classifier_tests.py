import requests
from mock import patch
from nose.tools import assert_true

from categorizer.email_classifier import EmailClassifier
from settings import TestAppConfig


class GoodResponse:
    status_code = 200
    content = '{"data": "working post request"}'

    def raise_for_status(self):
        return True


class TestEmailClassifier:

    @classmethod
    def setup(cls):
        cls._mock_settings = TestAppConfig()

    @patch.object(requests, 'post', return_value=GoodResponse())
    def test_get_predictions(self, mock_post):
        emc = EmailClassifier(self._mock_settings.categorizer_username,
                              self._mock_settings.categorizer_password,
                              self._mock_settings.email_api_url,
                              self._mock_settings.jwt_url, self._mock_settings.cert_path, self._mock_settings.key_path)
        assert_true(emc.get_prediction(('phishing subject', 'this is a phishing email')).status_code, True)
