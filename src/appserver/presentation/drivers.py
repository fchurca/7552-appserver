from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.persistence.mongodb.user import UserRepository

import json

import flask

logger = LoggerFactory().getLogger('DriversResource')
repository = UserRepository()

class DriversResource(Resource):
    def get(self):
        logger.info('method:GET')
        ret=list(repository.find({'type':'driver'}))
        return ret
