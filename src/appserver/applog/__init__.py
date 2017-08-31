## @package appserver.applog
#
# Define clases y utilidades para estandarizar el proceso de logging.

from appserver import appconfig

import logging
import sys

##
# Clase encargada de administrar la instanciación y configuración de los objetos
# Logger a ser utilizados por las demás entidades del sistema.
class LoggerFactory(object):
    
    _CONFIG = appconfig.APP_CONFIG.get_file('logging.ini')
    
    _LEVEL = _CONFIG.get('Logging', 'level', 'INFO')
    
    _FORMAT = _CONFIG.get('Logging', 'format' , '')
    
    logging.basicConfig(level=_LEVEL, format=_FORMAT)
    
    ##
    # @param name Nombre que identifica al logger.
    # @return Instancia de un Logger con el nombre recibido como argumento. 
    def getLogger(self, name):
        return logging.getLogger(name)