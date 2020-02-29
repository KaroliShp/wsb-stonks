import os
from pymongo import MongoClient


class MongoPostRepository(object):


    def __init__(self, database):
        mongo_url = os.environ.get('MONGO_URL')
        self.db = MongoClient(mongo_url)[database]


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