from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.auth import Auth
from appserver.persistence.mongodb.user import UserRepository
from appserver.remotes.sharedserver import SharedServerRemote

import json

import flask

remote = SharedServerRemote()
logger = LoggerFactory().getLogger('DriversResource')
repository = UserRepository()

def getOrDefault(key, array, default=None):
    if key in array:
        return array[key]
    else:
        return default

class DriversResource(Resource):
    def get(self):
        logger.info('method:GET')
        user = Auth.authenticate()
        if (user is None):
            logger.info('wrong username')
            return 'Wrong username and/or password', 401
        logger.info('Existing user')
        if user['type'] != 'passenger':
            logger.info('User not a passenger')
            return 'User not a passenger', 403
        logger.info('Existing passenger')
        if 'position' not in user:
            logger.info('User doesnt have position yet')
            return [], 200
        position = user['position']
        # TODO: filter by position
        rets=list(repository.find({'type':'driver'}))
        drivers = []
        for ret in rets:
            if 'position' in ret:
                driver = {
                        'userId':ret['ssId'],
                        'location':getOrDefault('position',ret),
                        'profile':{
                            'type':getOrDefault('type', ret),
                            'firstName':getOrDefault('firstName', ret),
                            'lastName':getOrDefault('lastName', ret),
                            'country':getOrDefault('country', ret),
                            'cars':getOrDefault('cars', ret, [])}}
                for car in driver['profile']['cars']:
                    car['model']=car['properties'][0]
                    car['patent']=car['properties'][1]
                    del(car['properties'])
                    del(car['owner'])
                    del(car['_ref'])
                drivers.append(driver)
        return drivers

