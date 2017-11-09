import string
import requests
from appserver.remotes.sharedserver import SHARED_CONFIG
from appserver.applog import LoggerFactory

logger = LoggerFactory().getLogger('SharedServerRemote')
url = SHARED_CONFIG.get_url()
token = SHARED_CONFIG.get_token()
userTemplate={
        '_ref': 0,
        'type':'',
        'username':'',
        'password':'',
        'fb':{'userId':'',
            'authToken':''},
        'firstName':'',
        'lastName':'',
        'country':'',
        'email':'',
        'birthdate':'',
        'images':[]}

class SharedServerRemote(object):
    def __init__(self):
        self.headers = {'x-access-token': token}

    def request(self, method, path, data={}):
        logger.info('request')
        uri = url + path
        logger.debug(uri)
        logger.debug(data)
        logger.debug(self.headers)
        r = requests.request(method, uri, headers=self.headers, json=data)
        logger.debug(r.__dict__)
        return r

    def get(self, path):
        logger.info('get')
        return self.request('GET', path)

    def post(self, path, data={}):
        logger.info('post')
        return self.request('POST', path, data)

    def put(self, path, data={}):
        logger.info('put')
        return self.request('PUT', path, data)

    def insertUser(self, data):
        logger.info('insertUser')
        userSpecifics = {
                '_ref': 'LEGACY',
                'type': 'new',
                'email': data['email'],
                'username': data['username'],
                'password': data['password']}
        userData = {**userTemplate, **userSpecifics}
        logger.debug(userData)
        return self.post('users', userData)

    def insertFacebookUser(self, data):
        logger.info('insertUser')
        userSpecifics = {
                '_ref': 'LEGACY',
                'type': 'new',
                'fb': data}
        userData = {**userTemplate, **userSpecifics}
        logger.debug(userData)
        return self.post('users', userData)

    def getUser(self, ssId):
        logger.info('getUser')
        return self.get('users/{}'.format(ssId))

    def validateUser(self, data):
        logger.info('validateUser')
        return self.post('users/validate', data)

    def updateUser(self, ssId, data):
        logger.info('updateUser')
        return self.put('users/{}'.format(ssId), data)

    def getCars(self, ssId):
        logger.info('getCars')
        return self.get('users/{}/cars'.format(ssId))

    def insertCar(self, ssUserId, data):
        logger.info('insertCar')
        logger.debug(data)
        return self.post('users/{}/cars'.format(ssUserId),data)

    def updateCar(self, ssUserId, data):
        logger.info('updateCar')
        logger.debug(data)
        return self.put('users/{}/cars/{}'.format(ssUserId, data['id']),data)

