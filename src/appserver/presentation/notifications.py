from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.auth import Auth
from appserver.persistence.mongodb.user import UserRepository

import json
import flask
import requests
import os

logger = LoggerFactory().getLogger('NotificationsResource')
repository = UserRepository()

FCM_URL='https://fcm.googleapis.com/fcm/send'
FCM_API_KEY = os.getenv('FCM_API_KEY')

class NotificationsResource(Resource):
    def post(self):
        user = Auth.authenticate()
        if (user is None):
            logger.info('Unauthorized')
            return 'Session expired', 401
        content = request.get_json()
        targetUser = repository.find_one_ssId(content['userId'])
        logger.debug(targetUser)
        headers={'Content-Type':'application/json',
                'Authorization':'key={}'.format(FCM_API_KEY)}
        data={'to':targetUser['fcmToken'],
                'data':{'type':content['type'],
                    'payload':content['payload']}}
        r = requests.post(FCM_URL, headers=headers, json=data)
        logger.debug(r)
        msgRes = None
        if (r.status_code == 200):
            msgRes = r.json()
            logger.debug(msgRes)
        if (msgRes != None):
            logger.debug('Message sent successfully')
        return r.status_code

