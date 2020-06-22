import os
import pymongo
import json
import time
from bson import json_util
import eventador as ev

MONGOSTR = os.getenv('MONGOSTR')
MONGODB = os.getenv('MONGODB')
MONGOCOL = os.getenv('MONGOCOL')

def initial_copy():
    """ touch all documents to produce an initial stream of data """
    client = pymongo.MongoClient(MONGOSTR)
    db = client[MONGODB]
    col = db[MONGOCOL]
    print("initial copy...")
    try:
        col.update_many({}, {"$set":{"TSlastUpdate":int(time.time())}})
        return 0
    except Exception as e:
        print(e)
        return 1

if __name__== "__main__":
    initial_copy()
