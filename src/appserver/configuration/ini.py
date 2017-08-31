import configparser
import os

class IniFile(object):

    def __init__(self, path):
        self.config = configparser.ConfigParser()
        self.config.read(path)
        
    def get(self, section, key, default_value):
        if self.has(section, key):
            return self.config.get(section, key)
        else:
            return default_value
    
    def get_int(self, section, key, default_value):
        return int(self.get(section, key, default_value))
        
    def has(self, section, key):
        return self.config.has_option(section, key)
        
        
class ConfigurationDir(object):
    
    def __init__(self, path):
        self.path = path
    
    def get_file(self, name):
        path = os.path.join(self.path, name)
        return IniFile(path)