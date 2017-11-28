import datetime
import dateutil.parser
import flask
import json
from bson import json_util
from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.persistence.mongodb.trip import TripRepository
from appserver.persistence.mongodb.user import UserRepository
from appserver.remotes.sharedserver import SharedServerRemote
from appserver.auth import Auth

logger = LoggerFactory().getLogger('TripsEstimateResource')
tripRepository = TripRepository()
userRepository = UserRepository()
ssRemote = SharedServerRemote()

class TripsEstimateResource(Resource):
    def post(self):
        logger.info('post')
        user = Auth.authenticate()
        if (user is None):
            logger.info('wrong username')
            return 'Wrong username and/or password', 401
        logger.info('existing user')
        if user['type'] != 'passenger':
            logger.info('user not a passenger')
            return 'You must be a passenger', 403
        logger.info('Existing passenger')
        content = request.get_json()
        r = ssRemote.estimateTrip(user['ssId'], content['start'], content['end'])
        if r.status_code != 200:
            logger.info('Error retrieving estimate from server')
            logger.debug(r.__dict__)
            return 'Error estimating trip cost', 500
        j = r.json()
        logger.debug(j)
        cost = j['cost']
        return cost, 200

