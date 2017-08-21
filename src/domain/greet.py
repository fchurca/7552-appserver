from persistence.mongodb.test import TestRepository

class GreetCase(object):
    
    def execute(self, name):
        TestRepository().retrieve_test_data()
        return name