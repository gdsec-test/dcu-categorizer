import os


class AppConfig(object):
    IRIS_WSDL = None
    IRIS_SERVER = None
    IRIS_PORT = None
    IRIS_DATABASE = 'iris'

    pwd = ''
    dbstring = ''
    wsdl_url = ''
    abuse_service_id = ''
    phish_service_id = ''
    mal_service_id = ''
    net_service_id = ''
    leo_service_id = ''
    childabuse_service_id = ''
    notation_user = ''
    phishstory_eid = '15550'
    ds_abuse_group_id = ''
    csa_group_id = ''
    dcu_group_id = ''
    leo_email_id = '391'
    abuse_email_id = '1256'
    categorizer_username = os.getenv('CATEGORIZER_USER')
    categorizer_password = os.getenv('CATEGORIZER_PASSWORD')
    cert_path = os.getenv('CATEGORIZER_CERT')
    key_path = os.getenv('CATEGORIZER_KEY')
    email_api_url = 'https://cerbo.godaddy.com/predict/email-classifier'
    jwt_url = 'https://sso.godaddy.com/v1/secure/api/token'

    def __init__(self):
        self.IRIS_USERNAME = os.getenv('IRIS_USERNAME', 'username')
        self.IRIS_PASSWORD = os.getenv('IRIS_PASSWORD', 'password')

        self.dbstring = 'DRIVER=FreeTDS;SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password};TDS_VERSION=8.0'.format(
            server=self.IRIS_SERVER, port=self.IRIS_PORT, database=self.IRIS_DATABASE, username=self.IRIS_USERNAME,
            password=self.IRIS_PASSWORD
        )


class DevelopmentAppConfig(AppConfig):
    IRIS_WSDL = 'https://iris-ws.dev.int.godaddy.com/iriswebService.asmx?WSDL'
    IRIS_SERVER = '10.32.76.23\\CSS'

    abuse_service_id = '220'
    phish_service_id = '212'
    mal_service_id = '213'
    net_service_id = '260'
    leo_service_id = '215'
    childabuse_service_id = '214'
    notation_user = 'rduran'
    ds_abuse_group_id = '489'
    csa_group_id = '510'
    dcu_group_id = '489'  # doesn't exist, using DS Abuse
    categorizer_username = os.getenv('CATEGORIZER_USER')
    categorizer_password = os.getenv('CATEGORIZER_PASSWORD')
    email_api_url = 'https://cerbo.godaddy.com/predict/email-classifier'
    jwt_url = 'https://sso.godaddy.com/v1/secure/api/token'
    cert_path = os.getenv('CATEGORIZER_CERT')
    key_path = os.getenv('CATEGORIZER_KEY')

    def __init__(self):
        super(DevelopmentAppConfig, self).__init__()


class ProductionAppConfig(AppConfig):
    IRIS_WSDL = 'https://iris-ws.int.godaddy.com/iriswebservice.asmx?wsdl'
    IRIS_SERVER = '10.32.146.30'
    IRIS_PORT = 1433

    abuse_service_id = '228'
    phish_service_id = '226'
    mal_service_id = '225'
    net_service_id = '232'
    leo_service_id = '224'
    childabuse_service_id = '221'
    notation_user = 'phishtory'
    ds_abuse_group_id = '411'
    csa_group_id = '443'
    dcu_group_id = '409'
    categorizer_username = os.getenv('CATEGORIZER_USER')
    categorizer_password = os.getenv('CATEGORIZER_PASSWORD')
    email_api_url = 'https://cerbo.godaddy.com/predict/email-classifier'
    jwt_url = 'https://sso.godaddy.com/v1/secure/api/token'
    cert_path = os.getenv('CATEGORIZER_CERT')
    key_path = os.getenv('CATEGORIZER_KEY')

    def __init__(self):
        super(ProductionAppConfig, self).__init__()


class TestAppConfig(AppConfig):

    categorizer_username = os.getenv('CATEGORIZER_USER')
    categorizer_password = os.getenv('CATEGORIZER_PASSWORD')
    cert_path = os.getenv('CATEGORIZER_CERT')
    key_path = os.getenv('CATEGORIZER_KEY')
    email_api_url = 'https://cerbo.godaddy.com/predict/email-classifier'
    jwt_url = 'https://sso.godaddy.com/v1/secure/api/token'

    def __init__(self):
        super(TestAppConfig, self).__init__()


config_by_name = {'dev': DevelopmentAppConfig,
                  'prod': ProductionAppConfig,
                  'test': TestAppConfig
                  }
