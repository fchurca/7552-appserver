from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.persistence.mongodb.user import UserRepository
from appserver.remotes.sharedserver.remote import SharedServerRemote

import json

import flask

remote = SharedServerRemote()
logger = LoggerFactory().getLogger('DriversResource')
repository = UserRepository()

class DriversResource(Resource):
    def get(self):
        remote.query('users')
        logger.info('method:GET')
        ret=list(repository.find({'type':'driver'}))
        return ret
