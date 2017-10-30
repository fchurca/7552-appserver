import re
from base64 import b64decode
from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.persistence.mongodb.user import UserRepository

import flask

logger = LoggerFactory().getLogger('UserResource')
repository = UserRepository()

class UserResource(Resource):
    def get(self):
        logger.info('method:GET')

        if (not 'Authorization' in request.headers):
            logger.warn('no authorizationHeader')
            return 'Missing Authorization header', 401
        authorizationHeader=request.headers['Authorization']
        logger.info('Authorization header: %s', authorizationHeader)
        if (not re.match(re.compile(r'^bearer\W', re.I), authorizationHeader)):
            logger.warn('no bearer')
            return 'Authorization header is not Bearer', 401
        tokenpayload = b64decode(re.compile(r'^bearer\s+(.*)$', re.I).sub(r'\1',authorizationHeader))
        logger.info('Tokenpayload: %s', tokenpayload)
        username,token=tokenpayload.decode('ascii').split('|')
        logger.info('Username: %s', username)
        logger.info('Token: %s', token)
        user = repository.find_one(username, {'password': False})
        if user['token'] != tokenpayload:
            logger.info('wrong token')
            return 'Session expired', 401
        else:
            logger.info('get user')
            del user['token']
            return user, 200
    def post(self):
        logger.info('method:POST')
        content = request.get_json()
        if (not 'Authorization' in request.headers):
            logger.info('No authorizationheader; new user')
            username=content['username']
            if (repository.find_one(username)):
                logger.warn('User exists')
                return 'User already exists', 409
            else:
                logger.debug('User didn\'t exist')
                if repository.insert(content):
                    logger.debug('Success')
                    return repository.find_one(username, {'token': False, 'password': False}), 202
                else:
                    logger.debug('Error')
                    return 'There was an error creating the user', 500
        else:
            authorizationHeader=request.headers['Authorization']
            logger.info('Authorization header: %s', authorizationHeader)
            if (not re.match(re.compile(r'^bearer\W', re.I), authorizationHeader)):
                logger.warn('no bearer')
                return 'Authorization header is not Bearer', 401
            tokenpayload = b64decode(re.compile(r'^bearer\s+(.*)$', re.I).sub(r'\1',authorizationHeader))
            logger.info('Tokenpayload: %s', tokenpayload)
            username,token=tokenpayload.decode('ascii').split('|')
            logger.info('Username: %s', username)
            logger.info('Token: %s', token)
            user = repository.find_one(username, {'password': False})
            if user['username'] != username:
                logger.info('wrong username')
                return 'Wrong username', 403
            if user['token'] != tokenpayload:
                logger.info('wrong token')
                return 'Session expired', 401
            logger.info('update user')
            if repository.update(username, content):
                return repository.find_one(username, {'token': False, 'password': False}), 202
            else:
                return "There was an error processing the request", 500

