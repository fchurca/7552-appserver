import datetime
import flask
from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.persistence.mongodb.trip import TripRepository
from appserver.persistence.mongodb.user import UserRepository
from appserver.auth import Auth

logger = LoggerFactory().getLogger('TripsResource')
tripRepository = TripRepository()
userRepository = UserRepository()

class TripsResource(Resource):
    def get(self):
        logger.info('get')
        user = Auth.authenticate()
        if (user is None):
            logger.info('wrong username')
            return 'Wrong username and/or password', 401
        logger.info('existing user')
        ret = list(tripRepository.find())
        logger.info('success')
        return ret, 200
    def post(self):
        logger.info('post')
        user = Auth.authenticate()
        if (user is None):
            logger.info('wrong username')
            return 'Wrong username and/or password', 401
        if ('type' not in user
                or user['type'] != 'driver'):
            logger.warn('Not a driver')
            return 'Not a driver', 403
        logger.info('existing driver')
        driver = user
        if ('trip_id' in driver
                and driver['trip_id'] is not None):
            logger.warn('Driver already in trip')
            return 'Driver already in trip', 403
        logger.debug('free driver')
        content = request.get_json()
        logger.debug(content)
        passenger = userRepository.find_one_ssId(content['passenger'])
        if (passenger is None):
            logger.warn('Passenger doesnt exist')
            return 'Passenger doesnt exist', 404
        if (passenger['type'] != 'passenger'):
            logger.warn('Passenger isnt a passenger')
            return 'Passenger isnt a passenger', 409
        if ('trip_id' in passenger
                and passenger['trip_id'] is not None):
            logger.warn('Passenger already in trip')
            return 'Passenger already in trip', 403
        logger.debug('free passenger')
        trip_id = tripRepository.insert({
            'state':'waiting',
            'times':{'accept':datetime.datetime.now().isoformat()},
            'driver_ssId':driver['ssId'],
            'passenger_ssId':passenger['ssId'],
            'start':content['start'],
            'end':content['end'],
            'route':[content['start']],
            'distance':0})
        if (trip_id is None):
            logger.warn('Trip insert failed')
            return 'Error creating trip', 500
        userRepository.update_ssId(driver['ssId'], {'trip_id':trip_id})
        userRepository.update_ssId(passenger['ssId'], {'trip_id':trip_id})
        logger.info('success')
        return tripRepository.find_one(trip_id), 200

