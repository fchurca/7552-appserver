import flask

from presentation.greet import GreetController

app = flask.Flask(__name__)

def handle(controller, pathvars):
    rq = flask.request
    
    controller_rs = controller.handle({
          'method'   : rq.method,
          'values'   : rq.values,
          'cookies'  : rq.cookies,
          'headers'  : rq.headers,
          'body'     : rq.data,
          'pathvars' : pathvars,
        })
    
    flask_response = flask.make_response(
        controller_rs['body'], 
        controller_rs['status'])
    
    return flask_response

@app.route('/greet/<name>')
def greet(name):
    return handle(GreetController(), { 'name' : name })