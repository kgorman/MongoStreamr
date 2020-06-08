import requests
import uuid
import os

print(1)
TOPIC      = os.getenv("TOPIC", "test")
BASE_URL   = os.getenv("URL")
CREATE_URL = "{}/kafka/topic/create".format(BASE_URL)
SEND_URL   = "{}/kafka/topic/{}/send".format(BASE_URL, TOPIC)
API_KEY    = os.getenv("API_KEY")

print(CREATE_URL)

## Status Codes
TOPIC_ALREADY_EXISTS = 409

def create_session():
    session = requests.Session()
    session.headers.update({
        "Authorization" : "Bearer " + API_KEY,
        "Content-Type": "application/json"
    })
    return session

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
        else:
            print("unable to create topic")

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
        response = create_topic(session)
        requestBody = createRequestBody(key, data)
        response    = session.post(SEND_URL, json = requestBody)
        response.raise_for_status()
        print(response.json())
    except Exception as e:
        print(e)
