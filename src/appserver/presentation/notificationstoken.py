import flask
import random
import requests
from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.auth import Auth
from appserver.persistence.mongodb.user import UserRepository

logger = LoggerFactory().getLogger('NotificationsTokenResource')
repository = UserRepository()

class NotificationsTokenResource(Resource):
    def post(self):
        user = Auth.authenticate()
        if (user is None):
            logger.info('Unauthorized')
            return 'Session expired', 401
        content = request.get_json()
        logger.debug(content)

        r = repository.update(user['username'], {'fcmToken':content['token']})
        logger.debug(r.raw_result)

        return 200

