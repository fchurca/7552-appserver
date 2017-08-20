from domain.greet import GreetCase

class GreetController(object):
    
    def handle(self, request):
        case = GreetCase()

        message = 'Hello, ' + case.execute(request['pathvars']['name'])
        
        return {'status' : 200, 'body' : message}