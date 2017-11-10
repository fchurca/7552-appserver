import flask
import flask_restful

from appserver.presentation.admin import AdminResource
from appserver.presentation.drivers import DriversResource
from appserver.presentation.position import PositionResource
from appserver.presentation.token import TokenResource
from appserver.presentation.user import UserResource

app = flask.Flask(__name__)
api = flask_restful.Api(app)

api.add_resource(AdminResource, '/admin/')
api.add_resource(DriversResource, '/drivers/')
api.add_resource(PositionResource, '/position/')
api.add_resource(TokenResource, '/token/')
api.add_resource(UserResource, '/user/')

