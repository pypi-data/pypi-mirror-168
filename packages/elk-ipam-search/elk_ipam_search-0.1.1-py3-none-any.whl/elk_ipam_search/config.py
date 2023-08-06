import os
from dotenv import load_dotenv

dirname = os.path.dirname
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv()


def convert_env_bool(string: str):
    return True if os.environ.get(string).lower() == 'true' else False


def convert_env_tuple(string: str):
    return tuple(os.environ.get(string).split(', '))


ELK_USER = os.environ.get('ELK_USER')
ELK_PASS = os.environ.get('ELK_PASS')
ELK_URL = os.environ.get('ELK_URL')
IPAM_TOKEN = os.environ.get('IPAM_TOKEN')
IPAM_URL = os.environ.get('IPAM_URL')
THEHIVE_URL = os.environ.get('THEHIVE_URL')
THEHIVE_API_TOKEN = os.environ.get('THEHIVE_API_TOKEN')
THEHIVE_EXTENSIONS = convert_env_tuple('THEHIVE_EXTENSIONS')
BOT_SERVER_URL = os.environ.get('BOT_SERVER_URL')
DEBUG = convert_env_bool('DEBUG')
CLICK_HOUSE = {
    'ip':  os.environ.get('CLICK_HOUSE_IP'),
    'port':  int(os.environ.get('CLICK_HOUSE_PORT')),
    'user':  os.environ.get('CLICK_HOUSE_USER'),
    'password':  os.environ.get('CLICK_HOUSE_PASS'),
    'db':  os.environ.get('CLICK_HOUSE_DB')
}
VOCABLIARY = {
    'ip': "IP адрес",
    'prefix': 'Подсеть',
    'aggregate': 'Сеть',
    'region': 'Регион',
    'tenant': 'Учреждение'
}
