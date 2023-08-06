
from urllib.parse import urljoin
from aishu import setting

def url(pathUrl):
    return urljoin('{http}://{ip}:{port}'.format(http=setting.testEnv_config['protocol'],ip=setting.testEnv_config['ip'],port=setting.testEnv_config['port']),pathUrl)