from persistence.mongodb.user import UserRepository

class GreetCase(object):
    
    def execute(self, name):
        UserRepository().save({ 'username' : name })
        return name