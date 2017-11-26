import flask
import flask_restful

from appserver.presentation.admin import AdminResource
from appserver.presentation.drivers import DriversResource
from appserver.presentation.notifications import NotificationsResource
from appserver.presentation.notificationstoken import NotificationsTokenResource
from appserver.presentation.position import PositionResource
from appserver.presentation.token import TokenResource
from appserver.presentation.trips import TripsResource
from appserver.presentation.trips_current import TripsCurrentResource
from appserver.presentation.user import UserResource

app = flask.Flask(__name__)
api = flask_restful.Api(app)

api.add_resource(AdminResource, '/admin/')
api.add_resource(DriversResource, '/drivers/')
api.add_resource(NotificationsResource, '/notifications/')
api.add_resource(NotificationsTokenResource, '/notifications/token/')
api.add_resource(PositionResource, '/position/')
api.add_resource(TokenResource, '/token/')
api.add_resource(TripsResource, '/trips/')
api.add_resource(TripsCurrentResource, '/trips/current/')
api.add_resource(UserResource, '/user/')

