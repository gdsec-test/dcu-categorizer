import os


class DevelopmentAppConfig():
    pwd = os.getenv('DEVIRISPWD') or 'password'
    dbstring = 'DRIVER={FreeTDS};SERVER=P3DWSQL07\CSS;DATABASE=iris;UID=N2_d338D4B45D0F445;PWD=' + pwd + ';TDS_VERSION=8.0'


class ProductionAppConfig():
    pwd = os.getenv('IRISPWD') or 'password'
    dbstring = 'DRIVER={FreeTDS};SERVER=10.32.146.30;PORT=1433;DATABASE=iris;UID=N1_mF09EAA138D464E;PWD=' + pwd + ';TDS_VERSION=8.0'

config_by_name = {'dev': DevelopmentAppConfig,
                  'prod': ProductionAppConfig
                  }
