import sys

'''
TODO: Implement decent logging capabilities
'''
class Logger(object):
    
    def info(self, *messages):
        for message in messages:
            sys.stdout.write(str(message))
        
        sys.stdout.flush()    
        print ''
        