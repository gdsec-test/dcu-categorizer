import json
import logging

import requests


class EmailClassifier:
    def __init__(self, categorizer_user, categorizer_pass, api_url, jwt_url, cert_path, key_path):
        self.api_url = api_url
        self.jwt_url = jwt_url
        self.jwt = self.get_token(categorizer_user, categorizer_pass, cert_path, key_path)
        self.cert_path = cert_path
        self.key_path = key_path

    def get_prediction(self, incident_dict):
        prediction_object = {
            'data': {
                'subject': incident_dict[0],
                'body': incident_dict[1]
            }
        }

        prediction_object = json.dumps(prediction_object)
        resp = requests.post(self.api_url, data=prediction_object, headers={'Authorization': 'sso-jwt ' + self.jwt},
                             timeout=15)
        if resp.status_code != 200:
            logging.error('status code other than 200. {}, message: {}'.format(resp.status_code, resp.content))
        return resp

    def get_token(self, user, password, cert_path, key_path):
        cert = (cert_path, key_path)
        request_body = {
            'realm': 'jomax',
            'username': user,
            'password': password
        }

        request_body = json.dumps(request_body)
        resp = requests.post(self.jwt_url, data=request_body,
                             cert=cert, headers={'content-type': 'application/json'}, timeout=15)
        if resp.status_code != 201:
            logging.error('status code other than 200. {}, message: {}'.format(resp.status_code, resp.content))

        to_dict = json.loads(resp.content)
        jwt = to_dict["data"]
        return jwt
