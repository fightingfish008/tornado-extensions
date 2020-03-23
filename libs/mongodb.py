# -*- coding:utf-8 -*-


import logging
import traceback

import urllib.parse
import motor.motor_tornado
from bson.objectid import ObjectId
from tornado.options import options


class AsyncMongoClient(object):
    def __init__(self, db=None):
        super(AsyncMongoClient, self).__init__()
        if db:
            _db = db
        else:
            _db = options.mongodb_database
        try:
            # print("mongodb ==={}===".format(options.as_dict()))
            username = urllib.parse.quote_plus(options.mongodb_user)
            password = urllib.parse.quote_plus(options.mongodb_password)
            uri = "mongodb://{}:{}@{}:{}/{}".format(
                username,
                password,
                options.mongodb_host,
                options.mongodb_port,
                _db
            )

            client = motor.motor_tornado.MotorClient(uri)
            self.client = client
            self.db = client[_db]
        except Exception as e:
            logging.error(traceback.print_exc())
            logging.error(e.args)
            # raise Exception('Unable to connect to MongoDB')

    async def insert_one(self, collection, document):
        """
        example: _id = await AsyncMongoClient.insert_one('test_collection', {'key': 'value'})
        """
        result = await self.db[collection].insert_one(document)
        return result.inserted_id

    async def insert_many(self, collection, documents):
        """
        example: count = await AsyncMongoClient.insert_many('test_collection', [{'i': i} for i in range(2000)])
        """
        result = await self.db[collection].insert_many(documents)
        return len(result.inserted_ids)

    async def count(self, collection, filter):
        """
        example: doc = await AsyncMongoClient.find_one('test_collection', {'i': {'$lt': 1}})
        """
        document = await self.db[collection].count_documents(filter)
        return document

    async def find_one(self, collection, filter):
        """
        example: doc = await AsyncMongoClient.find_one('test_collection', {'i': {'$lt': 1}})
        """
        document = await self.db[collection].find_one(filter)
        return document

    async def find(self, collection, filter, n=100):
        """
        example: doc = await AsyncMongoClient.find('test_collection', {'i': {'$lt': 5}})
        """
        docs = []
        cursor = self.db[collection].find(filter)
        for document in await cursor.to_list(length=n):
            docs.append(document)
        return docs

    async def findlimtskip(self, collection, filter, n=100):
        """
        example: c = await AsyncMongoClient.findlimtskip('test_collection',
                                                        [{'$match': {"doctor_id": _user_doctor["id"],
                                                                   "status": 1,
                                                                   # "sender": "p"
                                                                   }},
                                                       {'$sort': {'create_time': -1}},
                                                       {'$group': {'_id': {'patient_id': '$patient_id'},
                                                                   'data': {'$first': "$data"},
                                                                   'type': {'$first': "$type"},
                                                                   'create_time': {'$first': '$create_time'},
                                                                   'patient_id': {'$first': '$patient_id'},
                                                                   'doctor_id': {'$first': '$doctor_id'},
                                                                   'user_id': {'$first': '$user_id'},
                                                                   'sender': {'$first': '$sender'},
                                                                   'status': {'$first': '$status'},
                                                                   'id': {'$first': '$_id'}

                                                                   }},
                                                       {'$skip': 0},
                                                       {'$limit': 10}])
        """
        docs = []
        # myPipeline = {'$skip': 0}
        # SencondPipeline = {'$limit': 3}
        # ThirdPineline = {'$match': {"pharmacist.id": 1, 'status': 7}}
        # # # {"pharmacist.id": _user["id"],
        newfilter = []
        # for key, value in filter.items():
        #     newfilter.append({key: value})

        newfilter = filter
        cursor = self.db[collection].aggregate(newfilter)
        # cursor = self.db[collection].aggregate([ThirdPineline,myPipeline,SencondPipeline ])
        for document in await cursor.to_list(length=n):
            docs.append(document)
        return docs

    # aggregate
    async def aggregate(self, collection, filter, n=100):
        docs = []
        newfilter = filter
        cursor = self.db[collection].aggregate(newfilter)
        # cursor = self.db[collection].aggregate([ThirdPineline,myPipeline,SencondPipeline ])
        for document in await cursor.to_list(length=n):
            docs.append(document)
        return docs

    #update one document
    async def modify(self, collection, filter, mod_value_dict):
        """
        example: c = await AsyncMongoClient.update_one('test_collection', {'i': 51}, {'$set': {'key': 'value'}})
        """
        result = await self.db[collection].update_one(filter, {"$set": mod_value_dict})
        return result.modified_count
    
    #update many documents
    async def update(self, collection, filter, mod_value_dict):
        """
        example: c = await AsyncMongoClient.update_many('test_collection', {'i': {'$gt': 100}}, {'$set': {'key': 'value'}})
        """
        result = await self.db[collection].update_many(filter, {"$set": mod_value_dict})
        return result.modified_count

    async def delete(self, collection, filter):
        """
        example: doc = await AsyncMongoClient.find_one('test_collection', {'i': {'$lt': 1}})
        """
        result = await self.db[collection].delete_one(filter)
        return result.deleted_count

    new = insert_one

    def id_filter(self, id):
        return {'_id': ObjectId(id)}

def connect():
    async_mongo_client = AsyncMongoClient()
    return async_mongo_client
