import unittest

from appserver.configuration.envar import EnvironmentVariable 

class TestEnvironmentVariable(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def testExistingVariable(self):
        envar = EnvironmentVariable('TEST_VARIABLE')
        self.assertEqual(envar.get_value(), 'exists')
        
    def testNonExistingVariable(self):
        envar = EnvironmentVariable('TOST_VARIABLE')
        self.assertEqual(envar.get_value(), '')
