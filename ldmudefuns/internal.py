import os
import configparser

def get_config():
    config = configparser.ConfigParser()
    config['efuns'] = {}
    config['types'] = {}
    config.read(os.path.expanduser('~/.ldmud-efuns'))
    return config
