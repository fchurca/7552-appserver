from persistence.mongodb.test import TestRepository

class GreetCase(object):
    
    def execute(self, name):
        print 'Loaded test data: ' + TestRepository().retrieve_test_data()
        return name.capitalize()