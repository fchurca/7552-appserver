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

logger = LoggerFactory().getLogger('TripsCurrentResource')
tripRepository = TripRepository()
userRepository = UserRepository()
remote = SharedServerRemote()

class TripsCurrentResource(Resource):
    def get(self):
        logger.info('get')
        user = Auth.authenticate()
        if (user is None):
            logger.info('wrong username')
            return 'Wrong username and/or password', 401
        logger.info('existing user')
        if ('trip_id' not in user
                or user['trip_id'] is None):
            logger.warn('User not in trip')
            return 'User not in trip', 403
        logger.debug('user in trip')
        ret = tripRepository.find_one(user['trip_id'])
        logger.debug(ret)
        logger.info('success')
        return ret, 200
    def patch(self):
        logger.info('patch')
        user = Auth.authenticate()
        if (user is None):
            logger.info('wrong username')
            return 'Wrong username and/or password', 401
        logger.info('existing user')
        if ('trip_id' not in user
                or user['trip_id'] is None):
            logger.warn('User not in trip')
            return 'User not in trip', 403
        logger.debug('user in trip')
        trip_id = user['trip_id']
        trip = tripRepository.find_one(trip_id)
        logger.debug(trip)
        content = request.get_json()
        if ('state' not in content):
            logger.warn('No state reported')
            return 'No state reported', 400
        newState = content['state']
        if (newState not in ['IN_CAR', 'END']):
            logger.warn('Unrecognized state: {}'.format(newState))
            return 'New state unrecognized', 400
        if (newState == 'IN_CAR'):
            logger.info('IN_CAR')
            if (user['type'] != 'passenger'):
                logger.warn('User is not a passenger')
                return 'User is not a passenger', 403
            logger.debug('User is a passenger')
            if (trip['state'] != 'waiting'):
                logger.warn('Trip not waiting')
                return 'Trip not waiting', 400
            logger.debug('Trip was waiting')
            trip_times = trip['times']
            trip_times['in_car'] = datetime.datetime.now().isoformat()
            wait_time = (dateutil.parser.parse(trip_times['in_car']) - dateutil.parser.parse(trip_times['accept'])).total_seconds()
            tripRepository.update(trip_id, {
                'state':'in_car',
                'times':trip_times,
                'waitTime':wait_time})
        elif (newState == 'END'):
            logger.info('END')
            if (trip['state'] != 'in_car'):
                logger.warn('Trip not in_car')
                return 'Trip not in car', 400
            logger.debug('Trip was in car')
            trip_times = trip['times']
            trip_times['end'] = datetime.datetime.now().isoformat()
            travel_time = (dateutil.parser.parse(trip_times['end']) - dateutil.parser.parse(trip_times['in_car'])).total_seconds()
            total_time = (dateutil.parser.parse(trip_times['end']) - dateutil.parser.parse(trip_times['accept'])).total_seconds()

            r = remote.insertTrip({
                'trip':{
                    'driver':trip['driver_ssId'],
                    'passenger':trip['passenger_ssId'],
                    'start':{
                        'address':trip['start'],
                        'timestamp':int(dateutil.parser.parse(trip_times['in_car']).timestamp())},
                    'end':{
                        'address':trip['end'],
                        'timestamp':int(dateutil.parser.parse(trip_times['end']).timestamp())},
                    'distance':4200.0/1000.0, #TODO: calculate as float [kilometres]
                    'route':json.dumps(trip['route']),
                    'totalTime':int(total_time),
                    'waitTime':int(trip['waitTime']),
                    'travelTime':int(travel_time)},
                'paymethod':{ # TODO: bring from user profile?
                    'paymethod':'card',
                    'parameters':{
                        'ccvv':'123',
                        'expiration_month':'10',
                        'expiration_year':'2018',
                        'number':'1234-5678-8765-4321',
                        'type':'VISA'}}})
            if (r.status_code != 201):
                logger.debug(r.json())
                return r.json(), 500
            tripRepository.update(trip_id, {
                'state':'end',
                'times':trip_times,
                'travelTime':travel_time,
                'totalTime':total_time})
            userRepository.update_ssId(trip['driver_ssId'],{'trip_id':None})
            userRepository.update_ssId(trip['passenger_ssId'],{'trip_id':None})
            # TODO: Notify driver, passenger
        logger.info('success')
        return tripRepository.find_one(trip_id), 200
    def delete(self):
        logger.info('delete')
        user = Auth.authenticate()
        if (user is None):
            logger.info('wrong username')
            return 'Wrong username and/or password', 401
        logger.info('existing user')
        if ('trip_id' not in user
                or user['trip_id'] is None):
            logger.warn('User not in trip')
            return 'User not in trip', 403
        trip_id = user['trip_id']
        logger.debug('user in trip')
        trip = tripRepository.find_one(trip_id)
        logger.debug(trip)
        if ('state' not in trip
                or trip['state'] != 'WAITING'):
            logger.warn('Trip not waiting')
            return 'Trip not waiting', 400
        logger.debug('Trip waiting')
        tripRepository.update(trip_id,{'state':'CANCELLED'})
        userRepository.update_ssId(trip['driver_ssId'],{'trip_id':None})
        userRepository.update_ssId(trip['passenger_ssId'],{'trip_id':None})
        logger.info('success')
        return '', 200

