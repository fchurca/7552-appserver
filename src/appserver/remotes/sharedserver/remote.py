from appserver.remotes.sharedserver import SHARED_CONFIG
from appserver.applog import LoggerFactory
import requests
import string

logger = LoggerFactory().getLogger('SharedServerRemote')
url = SHARED_CONFIG.get_url()
token = SHARED_CONFIG.get_token()

class SharedServerRemote(object):
    def query(self, path):
        logger.info('query')
        uri = url + path
        headers = {'x-access-token': token}
        logger.debug(uri)
        logger.debug(headers)
        return requests.get(uri, headers=headers)

