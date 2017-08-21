from persistence.mongodb.test import TestRepository

class GreetCase(object):
    
    def execute(self, name):
        testdata = TestRepository().retrieve_test_data()
        return name + ' (loaded ' + testdata + ' from the database)' 