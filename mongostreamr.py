import os
import pymongo
import json
from bson import json_util
import eventador as ev

MONGOSTR = os.getenv('MONGOSTR')
MONGODB = os.getenv('MONGODB')
MONGOCOL = os.getenv('MONGOCOL')

def watch():
    """ watch the change stream """
    client = pymongo.MongoClient(MONGOSTR)
    db = client[MONGODB]
    col = db[MONGOCOL]

    change_stream = col.watch(full_document='updateLookup')
    print("watching for changes..")
    for change in change_stream:
        payload = json.loads(json.dumps(change['fullDocument'], default=json_util.default)) # handle bson types
        del payload['ts']
        del payload['_id']
        ev.produce(key=change['_id']['_data'], data=json.loads(json.dumps(payload, default=json_util.default)))
        print(json.dumps(payload, indent=4))
    return 0

if __name__== "__main__":
    ev.start_clean()
    watch()
