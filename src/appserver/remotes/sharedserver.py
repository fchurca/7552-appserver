from appserver.persistence.sharedserver import SHAREDSERVER_CONFIG
from appserver.applog import LoggerFactory

logger = LoggerFactory().getLogger('SharedServerRemote')
url = SHAREDSERVER_CONFIG.get_url()

class SharedServerRemote(object) :
    def idle ():
        return None

