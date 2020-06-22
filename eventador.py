import requests
import uuid
import os

TOPIC      = os.getenv("TOPIC", "test")
BASE_URL   = os.getenv("URL")
CREATE_URL = "{}/kafka/topic/create".format(BASE_URL)
DELETE_URL = "{}/kafka/topic/{}/delete".format(BASE_URL, TOPIC)
SEND_URL   = "{}/kafka/topic/{}/send".format(BASE_URL, TOPIC)
API_KEY    = os.getenv("API_KEY")

## Status Codes
TOPIC_ALREADY_EXISTS = 409

def create_session():
    session = requests.Session()
    session.headers.update({
        "Authorization" : "Bearer " + API_KEY,
        "Content-Type": "application/json"
    })
    return session

def delete_topic(session):
    try:
        response = session.delete(DELETE_URL)
        return response
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        print("unable to delete topic {}".format(TOPIC))
        return 1

def create_topic(session):
    try:
        response = session.post(CREATE_URL, json = {
            "topic" : TOPIC,
            "partitions": 1,
            "replicas": 1
        })
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        if status_code == TOPIC_ALREADY_EXISTS:
            print("Topic already exists, continuing normally")
            return status_code
        else:
            print("unable to create topic")
            return 1

def createRequestBody(k, d):
    return {
        "record": {
            "key" : k,
            "value" : d
        }
    }

def produce(key, data):
    try:
        session  = create_session()
        requestBody = createRequestBody(key, data)
        response    = session.post(SEND_URL, json = requestBody)
        response.raise_for_status()
        print(response.json())
    except Exception as e:
        print(e)

def start_clean():
    print("cleaning up..")
    try:
        session  = create_session()
        response = delete_topic(session)
        response = create_topic(session)
        print(response.json())
    except Exception as e:
        print(e)
