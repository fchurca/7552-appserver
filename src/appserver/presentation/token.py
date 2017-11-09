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
        if (content == None):
            return 'Malformed request', 400
        isLocal = 'username' in content and content['username'] != None
        isFacebook = 'facebookAuthToken' in content and content['facebookAuthToken'] != None
        username = None
        if (((not isLocal) and (not isFacebook))
            or (isLocal and isFacebook)
            or (isLocal and 'password' not in content)):
            return 'Malformed request', 400
        if isLocal:
            username = 'local:{}'.format(content['username'])
            user = repository.find_one(username)
            if (user is None):
                logger.info('wrong username')
                return 'Wrong username and/or password', 401
            logger.info('existing user')
            ssReq = {'username':content['username'], 'password':content['password']}
        else:
            fbToken = content['facebookAuthToken']
            ssReq = {'facebookAuthToken':fbToken}

        r = remote.validateUser(ssReq)
        logger.debug(r.__dict__)
        if (r.status_code == 412):
            logger.info('Precondition failed, creating user first')
            j = r.json()
            remote.insertFacebookUser({'userId':j['userId'], 'authToken':fbToken})
            r = remote.validateUser(ssReq)

        if (r.status_code != 200):
            logger.info('wrong password')
            return 'Wrong username and/or password', 401
        ssId = r.json()['user']['id']

        if (isFacebook):
            logger.info('facebook user')
            username = 'facebook:{}'.format(ssId)
            if (not repository.find_one(username)):
                logger.info('new facebook user')
                if not repository.insert({
                    'username':username,
                    'ssId':ssId}):
                    logger.info('Error')
                    return 'There was an error creating the user', 500

        logger.info('create token')
        token='{}|{}'.format(username,str(datetime.now())).encode('ascii')
        logger.debug('token: %s', token)
        if repository.update(username, {'token':token}):
            return {'token': base64.b64encode(token).decode('ascii')}, 202
        else:
            return None, 500

