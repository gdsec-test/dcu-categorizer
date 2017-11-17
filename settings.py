import os


class DevelopmentAppConfig():
    pwd = os.getenv('DEVIRISPWD') or 'password'
    dbstring = 'DRIVER={FreeTDS};SERVER=P3DWSQL07\CSS;DATABASE=iris;UID=N2_d338D4B45D0F445;PWD=' + pwd + ';TDS_VERSION=8.0'
    abuse_service_id = '220'
    phish_service_id = '212'
    mal_service_id = '213'
    net_service_id = '260'
    spam_service_id = '212' # doesn't exist, set to phishing


class ProductionAppConfig():
    pwd = os.getenv('IRISPWD') or 'password'
    dbstring = 'DRIVER={FreeTDS};SERVER=10.32.146.30;PORT=1433;DATABASE=iris;UID=N1_mF09EAA138D464E;PWD=' + pwd + ';TDS_VERSION=8.0'
    abuse_service_id = ''
    phish_service_id = ''
    mal_service_id = ''
    net_service_id = ''
    spam_service_id = ''

config_by_name = {'dev': DevelopmentAppConfig,
                  'prod': ProductionAppConfig
                  }
