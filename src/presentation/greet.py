from domain.greet import GreetCase
from applog import LoggerFactory

class GreetController(object):
    
    logger = LoggerFactory().getLogger('GreetController')
    
    def handle(self, request):
        name = request['pathvars']['name']
        GreetController.logger.info('Received name {}'.format(name))
        return {
            'status' : 200, 
            'body'   : 'Hello, ' + GreetCase().execute(name)
        }