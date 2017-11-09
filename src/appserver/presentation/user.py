import flask
import random
from flask import abort
from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.auth import Auth
from appserver.persistence.mongodb.user import UserRepository
from appserver.remotes.sharedserver.remote import SharedServerRemote

logger = LoggerFactory().getLogger('UserResource')
repository = UserRepository()
remote = SharedServerRemote()

class UserResource(Resource):
    def _get(self, user):
        r = remote.getUser(user['ssId'])
        logger.debug(r)
        if (r.status_code == 404):
            logger.warn('user nonexistent!')
            return None, 404
        if (r.status_code != 200):
            logger.warn('remote data unavailable!')
        user.update(r.json())
        r = remote.getCars(format(user['ssId']))
        logger.debug(r)
        if (r.status_code != 200):
            logger.warn('remote data unavailable!')
        ssCars = r.json()['cars']
        cars = []
        for ssCar in ssCars:
            properties = ssCar['properties']
            cars.append({
                'id': ssCar['id'],
                'model': properties[0],
                'patent': properties[1]})
        user.update({'cars': cars})
        logger.debug(user)
        return user, 200

    def get(self):
        logger.info('method:GET')
        user = Auth.authenticate()
        if (user is None):
            logger.info('Unauthorized')
            return 'Session expired', 401
        logger.info('local success')
        return self._get(user)

    def post(self):
        logger.info('method:POST')
        content = request.get_json()
        user=None
        if (not 'Authorization' in request.headers):
            logger.info('No authorizationheader; new user')
            username='local:{}'.format(content['username'])
            if (repository.find_one(username)):
                logger.warn('User exists')
                return 'User already exists', 409
            logger.debug('User didn\'t exist')
            r = remote.insertUser(content)
            logger.debug(r.__dict__)
            if r.status_code != 201:
                logger.info('sharedserver error')
                return 'There was an error creating the user', 500
            logger.info('sharedserver user creation succeeded')

            ssId = r.json()['user']['id']
            if not repository.insert({'username':username,'ssId':ssId}):
                logger.info('Error')
                return 'There was an error creating the user', 500
            user = repository.find_one(username)
            logger.info('Success')

        else:
            logger.info('update user')
            user = Auth.authenticate()
            if (user is None):
                logger.info('Unauthorized')
                return 'Session expired', 401
            username = user['username']
            ssId = user['ssId']
            r = remote.getUser(ssId)
            if r.status_code != 200:
                logger.warn('error getting remote user')
                return 'Error retrieving remote user from sharedserver', 400
            logger.info('remote user retrieved')
            logger.debug(r.json())
            data = {**r.json(), **user}
            data = {**data, **content}
            del data['ssId']
            del data['password']
            cars = None
            if 'cars' in data:
                cars = data['cars']
                del data['cars']
            logger.debug(data)
            r = remote.updateUser(ssId, data)
            logger.debug(r.__dict__)
            if r.status_code != 200:
                logger.warn('error updating remote user')
                return 'Error updating remote user on sharedserver', 400
            for car in cars:
                logger.debug(car)
                carModel = car['model']
                carPatent = car['patent']
                ssCar = {
                    'owner': ssId,
                    'properties':[carModel, carPatent]}
                if ('id' in car and car['id'] != None):
                    ssCar['id'] = car['id']
                    logger.debug(remote.updateCar(ssId, ssCar))
                else:
                    logger.debug(remote.insertCar(ssId, ssCar))

        return self._get(user)

