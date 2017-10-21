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
        ret=list(repository.find())
        logger.info(ret)
        return ret
    def post(self):
        logger.info('method:POST')
        content = request.get_json()
        if 'username' not in content:
            return 'Malformed request', 400
        key = content['username']
        user = repository.find_one(key)
        if (user):
            if (not 'Authorization' in request.headers):
                logger.warn('no authorizationHeader')
                return 'Missing Authorization header', 401
            authorizationHeader=request.headers['Authorization']
            logger.info('Authorization header: %s', authorizationHeader)
            if (not re.match(re.compile(r'^bearer\W', re.I), authorizationHeader)):
                logger.warn('no bearer')
                return 'Authorization header is not Bearer', 401
            token = b64decode(re.compile(r'^bearer\s+(.*)$', re.I).sub(r'\1',authorizationHeader))
            logger.info('Token: %s', token)
            logger.info('existing user')
            if user['token'] != token:
                logger.info('wrong token')
                return 'Session expired', 401
            else:
                logger.info('update user')
                if repository.update(key, content):
                    return repository.find_one(key, {'token': False, 'password': False}), 202
                else:
                    return None, 500
        else:
            logger.info('new user')
            if repository.insert(content):
                return repository.find_one(key), 201
            else:
                return None, 500

