import os


class DevelopmentAppConfig():
    pwd = os.getenv('DEVIRISPWD') or 'password'
    dbstring = 'DRIVER={FreeTDS};SERVER=P3DWSQL07\CSS;DATABASE=iris;UID=N2_d338D4B45D0F445;PWD=' + pwd + ';TDS_VERSION=8.0'
    wsdl_url = 'https://iris-ws.dev.int.godaddy.com/iriswebService.asmx?WSDL'
    abuse_service_id = '220'
    phish_service_id = '212'
    mal_service_id = '213'
    net_service_id = '260'
    spam_service_id = '212' # doesn't exist, set to phishing
    leo_service_id = '215'
    notation_user = 'rduran'


class ProductionAppConfig():
    pwd = os.getenv('IRISPWD') or 'password'
    dbstring = 'DRIVER={FreeTDS};SERVER=10.32.146.30;PORT=1433;DATABASE=iris;UID=N1_mF09EAA138D464E;PWD=' + pwd + ';TDS_VERSION=8.0'
    wsdl_url = 'https://iris-ws.int.godaddy.com/iriswebservice.asmx?wsdl'
    abuse_service_id = '228'
    phish_service_id = '226'
    mal_service_id = '225'
    net_service_id = '232'
    spam_service_id = '315'
    leo_service_id = '224'
    notation_user = 'phishtory'

config_by_name = {'dev': DevelopmentAppConfig,
                  'prod': ProductionAppConfig
                  }
