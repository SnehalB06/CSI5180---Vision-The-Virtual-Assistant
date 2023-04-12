import configparser

config = configparser.ConfigParser()
config.read('Config/config.ini')

def getConfigKey(keyName):
    return config.get('api_keys', keyName)