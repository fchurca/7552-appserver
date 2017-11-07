import flask
from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.persistence.mongodb.user import UserRepository
from appserver.auth import Auth

logger = LoggerFactory().getLogger('PositionResource')
repository = UserRepository()

class PositionResource(Resource):
    def post(self):
        logger.info('post')
        user = Auth.authenticate()
        if (user is None):
            logger.info('wrong username')
            return 'Wrong username and/or password', 401
        logger.info('existing user')
        content = request.get_json()
        latitude = content['latitude']
        longitude = content['longitude']
        username = user['username']
        data={
                'position':{
                    'latitude':latitude,
                    'longitude':longitude}}
        logger.debug(data)
        if not repository.update(username, data):
            return "There was an error processing the request", 500
        logger.info('success')
        return '', 200

