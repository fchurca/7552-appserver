import configuration.envar
import configuration.ini

class _AppServerConfiguration(object):
    
    APPSERVER_CFG = 'APPSERVER_CFG'
    
    def __init__(self):
        config_path = self.get_configuration_path()
        self._config_dir = configuration.ini.ConfigurationDir(config_path)
        
    def get_configuration_path(self):
        var_name = _AppServerConfiguration.APPSERVER_CFG
        var = configuration.envar.EnvironmentVariable(var_name)
        return var.get_value()

    def get_file(self, filename):
        return self._config_dir.get_file(filename)
    
APP_CONFIG = _AppServerConfiguration()