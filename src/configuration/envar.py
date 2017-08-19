import os

class EnvironmentVariable(object):

    def __init__(self, name):
        self.value = os.environ[name]
        
    def get_value(self):
        return self.value