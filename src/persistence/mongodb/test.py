from persistence.mongodb import MONGO_CONFIG

class TestRepository(object):
    
    _COLLECTION = 'test'
    
    def retrieve_test_data(self):
        cn = MONGO_CONFIG.get_connection()
        db = MONGO_CONFIG.get_database_from(cn)
        
        test_data = db[TestRepository._COLLECTION].find_one()
        
        cn.close()
        return test_data.get('testdata') if test_data else None