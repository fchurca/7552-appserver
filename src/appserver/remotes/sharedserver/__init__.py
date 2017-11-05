from appserver import appconfig
from appserver.configuration.envar import EnvironmentVariable

import os

class _SharedServerConfig(object):
    
    SHAREDSERVER_CONFIG = 'sharedserver.ini'
    
    SECTION_CONNECTION = 'Connection'

    KEY_SHARED_VAR = 'sharedservervar'
    KEY_SHARED_VAR_DEFAULT = None
    
    KEY_URL = 'url'
    KEY_URL_DEFAULT = 'http://localhost:5000/api/'

    TOKEN_VAR = 'SHAREDSERVER_TOKEN'
    
    def __init__(self):
        config = appconfig.APP_CONFIG.get_file(self.SHAREDSERVER_CONFIG)
            
        self._url = config.get(
            _SharedServerConfig.SECTION_CONNECTION,
            _SharedServerConfig.KEY_URL,
            _SharedServerConfig.KEY_URL_DEFAULT)
        self._token = EnvironmentVariable(_SharedServerConfig.TOKEN_VAR).get_value()

    def _load_url(self, config):
        sharedserver_var = config.get(
            _SharedServerConfig.SECTION_CONNECTION,
            _SharedServerConfig.KEY_SHARED_VAR,
            _SharedServerConfig.KEY_SHARED_VAR_DEFAULT)

        if not sharedserver_var:
            return config.get(
                _SharedServerConfig.SECTION_CONNECTION,
                _SharedServerConfig.KEY_URL,
                _SharedServerConfig.KEY_URL_DEFAULT)
        else:
            return EnvironmentVariable(sharedserver_var).get_value()

    def get_token(self):
        return self._token

    def get_url(self):
        return self._url

SHARED_CONFIG = _SharedServerConfig()
