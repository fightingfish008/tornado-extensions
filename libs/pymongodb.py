import pymongo
import datetime
import logging
import traceback

import urllib.parse


config = {"mongodb_host":"xxxxxxx",
          "mongodb_port":"xxxxxxx",
          "mongodb_database":"xxxxxxxx",
          "mongodb_user":"xxxxxxxx",
          "mongodb_password":"xxxxxxxx",
          "mongodb_rxtablesname":"xxxxxxxx"
        }


class AsyncMongoClient(object):
    def __init__(self, db=None):
        super(AsyncMongoClient, self).__init__()
        if db:
            _db = db
        else:
            _db = config["mongodb_database"]
        try:
            username = urllib.parse.quote_plus(config["mongodb_user"])
            password = urllib.parse.quote_plus(config["mongodb_password"])
            uri = "mongodb://{}:{}@{}:{}/{}".format(
                username,
                password,
                config["mongodb_host"],
                config["mongodb_port"],
                _db
            )

            # client = motor.motor_tornado.MotorClient(uri)
            client = pymongo.MongoClient(uri)
            self.client = client
            self.db = client[_db]
        except Exception as e:
            logging.error(traceback.print_exc())
            logging.error(e.args)
            # raise Exception('Unable to connect to MongoDB')

def connect():
    async_mongo_client = AsyncMongoClient()
    return async_mongo_client


def list(cursor):
    for c in cursor:
        print(c)

def pycollection():
    username = urllib.parse.quote_plus(config["mongodb_user"])
    password = urllib.parse.quote_plus(config["mongodb_password"])
    _db = config["mongodb_database"]
    uri = "mongodb://{}:{}@{}:{}/{}".format(
        username,
        password,
        config["mongodb_host"],
        config["mongodb_port"],
        _db
    )
    client = pymongo.MongoClient(uri)
    # client = pymongo.MongoClient('192.168.1.1',27017)
    # db = client.rxdb
    # db.authenticate("xxxxxx","xxxxxx")
    collection = client[_db]
    # t = collection.rx
    #
    # list(t.find())
    #
    #
    # # myDatetime1 = datetime.datetime().now()
    #
    #
    #
    # dateStr = '2018-06-12T00:00:00.000Z'
    # myDatetime = parser.parse(dateStr)
    #
    #
    # print('======',myDatetime)
    # # t.insert({'date': myDatetime})
    #
    # temp = datetime.datetime(2017, 9, 10, 0, 0)
    # # c = t.find({'create_time':{'$gte':temp}})
    # c = t.find({'doctor.id':2})
    # list(c)
    return collection


if __name__ == '__main__':
    t = pycollection()
    c = t['rx'].find().limit(10).sort('create_time', 1)
    list(c)


