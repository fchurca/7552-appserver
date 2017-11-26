from appserver.persistence.mongodb import MONGO_CONFIG
from appserver.applog import LoggerFactory
from bson import ObjectId

logger = LoggerFactory().getLogger('TripRepository')
cn = MONGO_CONFIG.get_connection()
db = MONGO_CONFIG.get_database_from(cn)
collection=db.trips

class TripRepository(object):
    def __init__(self):
        self.collection = collection
    def insert(self, trip):
        logger.info('insert')
        trip = collection.insert_one(trip)
        return None if trip is None else str(trip.inserted_id)
    def update(self, trip_id, payload):
        logger.info('update')
        logger.debug(trip_id)
        return collection.update_one({'_id': ObjectId(trip_id)}, {'$set':payload})
    def find(self, filter = {}, projection={}):
        logger.info('find')
        logger.debug(filter)
        projection['_id'] = False
        return collection.find(filter, projection)
    def find_one(self, trip_id, projection={}):
        logger.info('find_one')
        logger.debug(trip_id)
        projection['_id'] = False
        return collection.find_one({'_id': ObjectId(trip_id)}, projection)

