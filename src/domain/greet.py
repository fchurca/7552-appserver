from persistence.mongodb.test import TestRepository
from applog import LoggerFactory

class GreetCase(object):
    
    logger = LoggerFactory().getLogger('GreetCase')
    
    def execute(self, name):
        test_data = TestRepository().retrieve_test_data()
        self.logger.info('Loaded test data: {}'.format(test_data))    
        return name.capitalize()