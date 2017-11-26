import requests
import os
from appserver.applog import LoggerFactory

FCM_URL='https://fcm.googleapis.com/fcm/send'
FCM_API_KEY = os.getenv('FCM_API_KEY')

logger = LoggerFactory().getLogger('FCMRemote')

class FCMRemote(object):
    def notify(self, user, payload):
        logger.info('Notify')
        headers={'Content-Type':'application/json',
                'Authorization':'key={}'.format(FCM_API_KEY)}
        data={'to':user['fcmToken'],
                'data':payload}
        logger.debug(headers)
        logger.debug(data)
        r = requests.post(FCM_URL, headers=headers, json=data)
        logger.debug(r.__dict__)
        return r

