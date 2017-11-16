from appserver import appconfig
from appserver.configuration.envar import EnvironmentVariable

import os

class _FCMConfig(object):
    
    FCM_CONFIG = 'sharedserver.ini'
    
    SECTION_CONNECTION = 'Connection'

    KEY_SHARED_VAR = 'sharedservervar'
    KEY_SHARED_VAR_DEFAULT = None
    
    KEY_URL = 'url'
    KEY_URL_DEFAULT = 'http://localhost:5000/api/'

    TOKEN_VAR = 'FCM_TOKEN'
    
    def __init__(self):
        config = appconfig.APP_CONFIG.get_file(self.FCM_CONFIG)
            
        url = None
        sharedserver_var = config.get(
            _FCMConfig.SECTION_CONNECTION,
            _FCMConfig.KEY_SHARED_VAR,
            _FCMConfig.KEY_SHARED_VAR_DEFAULT)
        if not sharedserver_var:
            url = config.get(
                _FCMConfig.SECTION_CONNECTION,
                _FCMConfig.KEY_URL,
                _FCMConfig.KEY_URL_DEFAULT)
        else:
            url = EnvironmentVariable(sharedserver_var).get_value()
        self._url = url
        self._token = EnvironmentVariable(_FCMConfig.TOKEN_VAR).get_value()

    def get_token(self):
        return self._token

    def get_url(self):
        return self._url

SHARED_CONFIG = _FCMConfig()
