import appconfig

class _MongoConfig(object):
    
    MONGODB_CONFIG = 'mongo.ini'
    
    SECTION_CONNECTION = 'Connection'
    
    KEY_URI = 'uri'
    KEY_URI_DEFAULT = 'mongodb://localhost:27017'
    
    KEY_DB_NAME = 'db'
    KEY_DB_NAME_DEFAULT = 'db'
    
    def __init__(self):
        config = appconfig.APP_CONFIG.get_file(self.MONGODB_CONFIG)
        
        self._connection_string = config.get(
             _MongoConfig.SECTION_CONNECTION,
             _MongoConfig.KEY_URI,
             _MongoConfig.KEY_URI_DEFAULT)
            
        self._database_name = config.get(
            _MongoConfig.SECTION_CONNECTION,
            _MongoConfig.KEY_DB_NAME,
            _MongoConfig.KEY_DB_NAME_DEFAULT)
    
    def get_connection_string(self):
        return self._connection_string
    
    def get_database_name(self):
        return self._database_name
    
MONGO_CONFIG = _MongoConfig()