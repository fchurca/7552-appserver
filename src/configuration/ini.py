import ConfigParser
import os

class IniFile(object):

    def __init__(self, path):
        self.config = ConfigParser.ConfigParser()
        self.config.read(path)
        
    def get(self, section, key):
        return self.config.get(section, key)
    
    def get_integer(self, key):
        int(self.get(key))
        
        
class ConfigurationDir(object):
    
    def __init__(self, path_variable):
        self.dir_path = path_variable.get_value()
    
    def get_file(self, name):
        path = os.path.join(self.dir_path, name)
        return IniFile(path)