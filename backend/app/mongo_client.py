import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, BulkWriteError


class MongoPostRepository(object):


    def __init__(self, database, logger_ref):
        mongo_url = os.environ.get('MONGO_URL')
        client = MongoClient(mongo_url)
        self.logger = logger_ref
        
        try:
            # Check if connected to MongoDB Atlas
            # The ismaster command is cheap and does not require auth.
            client.admin.command('ismaster')
        except ConnectionFailure as e:
            self.logger.warning("MongoDB Server not available")
            self.logger.warning(e)

        self.db = client[database]


    def find_all(self, collection, selector):
        results = []

        cursor = self.db[collection].find(selector)
        for item in cursor:
            item['_id'] = str(item['_id'])
            results.append(item)
        
        return results


    def find(self, collection, selector):
        return self.db[collection].find_one(selector)


    def create(self, collection, item):
        return self.db[collection].insert_one(item)
    

    def create_many(self, collection, items):
        try:
            self.db[collection].insert_many(items, ordered=False)
        except BulkWriteError as e:
            self.logger.warning('MongoDB BulkWrite Error')
            self.logger.warning(e)


    def update(self, collection, selector, item):
        self.db[collection].replace_one(selector, item)


    def delete_many(self, collection, selector):
        self.db[collection].delete_many(selector)