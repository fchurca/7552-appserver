import base64
from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.persistence.mongodb.user import UserRepository

import flask
from datetime import datetime

logger = LoggerFactory().getLogger('TokenResource')
repository = UserRepository()

class TokenResource(Resource):
    def post(self):
        logger.info('method:POST')
        content = request.get_json()
        if (content == None
                or 'username' not in content
                or 'password' not in content):
            return 'Malformed request', 400
        key = content['username']
        user = repository.find_one(key)
        if (user):
            logger.info('existing user')
            if user['password'] != content['password']:
                logger.info('wrong password')
                return 'Wrong username and/or password', 401
            else:
                logger.info('create token')
                token=str(datetime.now()).encode('ascii')
                logger.debug('token: %s', token)
                if repository.update(key, {'token':token}):
                    return base64.b64encode(token).decode('ascii'), 202
                else:
                    return None, 500
        else:
            logger.info('wrong username')
            return 'Wrong username and/or password', 401

