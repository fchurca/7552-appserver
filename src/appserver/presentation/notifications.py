from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.auth import Auth
from appserver.persistence.mongodb.user import UserRepository
from appserver.remotes.fcm import FCMRemote

import json

logger = LoggerFactory().getLogger('NotificationsResource')
repository = UserRepository()
remote = FCMRemote()

class NotificationsResource(Resource):
    def post(self):
        user = Auth.authenticate()
        if (user is None):
            logger.info('Unauthorized')
            return 'Session expired', 401
        content = request.get_json()
        targetUser = repository.find_one_ssId(content['userId'])
        logger.debug(targetUser)
        r = remote.notify(targetUser, {
            'type':content['type'],
            'payload':content['payload']})
        logger.debug(r)
        msgRes = None
        if (r.status_code == 200):
            msgRes = r.json()
            logger.debug(msgRes)
        if (msgRes != None):
            logger.debug('Message sent successfully')
        return r.status_code

