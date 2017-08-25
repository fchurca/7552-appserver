import appconfig
import logging
import sys

class LoggerFactory(object):
    
    _CONFIG = appconfig.APP_CONFIG.get_file('logging.ini')
    
    _LEVEL = _CONFIG.get('Logging', 'level', 'INFO')
    
    _FORMAT = _CONFIG.get('Logging', 'format' , '')
    
    logging.basicConfig(level=_LEVEL, format=_FORMAT)
    
    def getLogger(self, name):
        return logging.getLogger(name)