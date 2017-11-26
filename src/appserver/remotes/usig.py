import requests
from appserver.applog import LoggerFactory

USIG_URL='https://servicios.usig.buenosaires.gob.ar/normalizar/'

logger = LoggerFactory().getLogger('USIGRemote')

class USIGRemote(object):
    def normalizar(self, payload):
        logger.info('Normalizar')
        logger.debug(payload)
        r = requests.get(USIG_URL, params=payload)
        logger.debug(r.__dict__)
        return r

