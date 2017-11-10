import flask
import os
from flask import request
from flask_restful import Resource
from appserver.applog import LoggerFactory
from appserver.persistence.mongodb import MONGO_CONFIG

logger = LoggerFactory().getLogger('AdminResource')
cn = MONGO_CONFIG.get_connection()
db = MONGO_CONFIG.get_database_from(cn)
collection=db.users

class AdminResource(Resource):
    def post(self):
        logger.info(':POST')
        logger.debug(collection.drop())
        return None, 200

