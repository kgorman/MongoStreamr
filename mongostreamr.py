import os
import pymongo
import json
from bson import json_util
import eventador as ev

MONGOSTR = os.getenv('MONGOSTR')
MONGODB = os.getenv('MONGODB')
MONGOCOL = os.getenv('MONGOCOL')

def main():
    client = pymongo.MongoClient(MONGOSTR)
    db = client[MONGODB]
    col = db[MONGOCOL]
    change_stream = col.watch()
    for change in change_stream:
        print(json.dumps(change['_id']['_data'], default=json_util.default, indent=4))
        ev.produce(key=change['_id']['_data'], data=json.loads(json.dumps(change['fullDocument'], default=json_util.default)))
    return 0

if __name__== "__main__":
    print("waiting...")
    main()
