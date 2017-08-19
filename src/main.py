from configuration import ini, envar

_APPSERVER_CFG = envar.EnvironmentVariable('APPSERVER_CFG')

if __name__ == '__main__':
    config_file = ini.ConfigurationDir(_APPSERVER_CFG).get_file("server.ini")
    print config_file.get("Network", "port")