from persistence.mongodb import MONGO_CONFIG

class UserRepository(object):
    
    _COLLECTION_NAME = "users"

    def save(self, user):
        cn = MONGO_CONFIG.get_connection()
        db = MONGO_CONFIG.get_database_from(cn)
        
        user_id = db[UserRepository._COLLECTION_NAME].insert_one(user)
        
        cn.close()
        return None if user_id == None else str(user_id)