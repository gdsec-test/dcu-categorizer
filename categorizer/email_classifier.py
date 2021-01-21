import requests
import os


class EmailClassifier:
    def __init__(self, vps4_user, vps4_password):
        self.api_url = "https://cerbo.godaddy.com/predict/email-classifier"
        self.jwt_url = os.getenv("JWT_URL")
        self.jwt = self.get_token(vps4_user, vps4_password)

    def get_prediction(self, incident_dict):
        prediction_object = {
            "data": {
                "subject": incident_dict[0],
                "body": incident_dict[1]
            }
        }

        resp = requests.post(self.api_url, data=prediction_object, headers={'Authorization': self.jwt})
        return resp

    def get_token(self, user, password):
        request_body = {
            "realm": "jomax",
            "username": user,
            "password": password
        }
        resp = requests.post(self.jwt_url, data=request_body, verify="certs/vps4.dev.client.int.godaddy.com.pem")
        return resp
