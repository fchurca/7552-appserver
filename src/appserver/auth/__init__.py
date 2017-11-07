import re
from base64 import b64decode
from flask import request
from appserver.applog import LoggerFactory
from appserver.persistence.mongodb.user import UserRepository

logger = LoggerFactory().getLogger('Auth')
repository = UserRepository()

class Auth(object):
    def authenticate():
        if (not 'Authorization' in request.headers):
            logger.warn('no authorizationHeader')
            return None
        authorizationHeader=request.headers['Authorization']
        logger.info('Authorization header: %s', authorizationHeader)
        if (not re.match(re.compile(r'^bearer\W', re.I), authorizationHeader)):
            logger.warn('no bearer')
            return None
        tokenpayload = b64decode(re.compile(r'^bearer\s+(.*)$', re.I).sub(r'\1',authorizationHeader))
        logger.info('Tokenpayload: %s', tokenpayload)
        logger.debug(tokenpayload.decode('ascii').split('|'))
        username, token =  tokenpayload.decode('ascii').split('|')
        user = repository.find_one(username, {'password': False})
        if user is None:
            logger.info('no user')
            return None
        if user['token'] != tokenpayload:
            logger.info('wrong token')
            return None
        else:
            logger.info('correct')
            del user['token']
            return user

