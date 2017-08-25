import appconfig
import pymongo

from configuration.envar import EnvironmentVariable

class _MongoConfig(object):
    
    MONGODB_CONFIG = 'mongo.ini'
    
    SECTION_CONNECTION = 'Connection'
    
    KEY_MONGO_VAR = 'mongovar'
    KEY_MONGO_VAR_DEFAULT = None
    
    KEY_URI = 'uri'
    KEY_URI_DEFAULT = 'mongodb://localhost:27017'
    
    KEY_DB_NAME = 'db'
    KEY_DB_NAME_DEFAULT = 'db'
    
    def __init__(self):
        config = appconfig.APP_CONFIG.get_file(self.MONGODB_CONFIG)
            
        self._database_name = config.get(
            _MongoConfig.SECTION_CONNECTION,
            _MongoConfig.KEY_DB_NAME,
            _MongoConfig.KEY_DB_NAME_DEFAULT)

        self._connection_string = self._load_connection_string(config)
    
    def _load_connection_string(self, config):
        mongo_var = config.get(
            _MongoConfig.SECTION_CONNECTION,
            _MongoConfig.KEY_MONGO_VAR,
            _MongoConfig.KEY_MONGO_VAR_DEFAULT)
        
        if not mongo_var:
            return config.get(
                _MongoConfig.SECTION_CONNECTION,
                _MongoConfig.KEY_URI,
                _MongoConfig.KEY_URI_DEFAULT)
        else:
            return EnvironmentVariable(mongo_var).get_value()

    def get_connection_string(self):
        return self._connection_string
    
    def get_database_name(self):
        return self._database_name
    
    def get_database_from(self, connection):
        return connection[self.get_database_name()]
    
    def get_connection(self):
        return pymongo.MongoClient(self.get_connection_string())
    
MONGO_CONFIG = _MongoConfig()
