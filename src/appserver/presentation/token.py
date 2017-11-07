import base64
from datetime import datetime

import flask
from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.persistence.mongodb.user import UserRepository
from appserver.remotes.sharedserver.remote import SharedServerRemote

logger = LoggerFactory().getLogger('TokenResource')
repository = UserRepository()
remote = SharedServerRemote()

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
        if (user is None):
            logger.info('wrong username')
            return 'Wrong username and/or password', 401
        logger.info('existing user')

        r = remote.validateUser({
            'username':content['username'],
            'password':content['password']})

        logger.debug(r)

        if (r.status_code != 200):
            logger.info('wrong password')
            return 'Wrong username and/or password', 401
        else:
            logger.info('create token')
            token='{}|{}'.format(user['username'],str(datetime.now())).encode('ascii')
            logger.debug('token: %s', token)
            if repository.update(key, {'token':token}):
                return {'token': base64.b64encode(token).decode('ascii')}, 202
            else:
                return None, 500

