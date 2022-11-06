#! /usr/local/bin/python3

import requests
import json
import pprint
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, storage


cred = credentials.Certificate(
    "weather-data-storage-c33f7-firebase-adminsdk-z15ho-415ecaf7dd.json")
app = firebase_admin.initialize_app(
    cred, {'databaseURL': 'https://weather-data-storage-c33f7-default-rtdb.europe-west1.firebasedatabase.app'})



api_key = open('api_key.txt').readline()

r = requests.get('https://api.waqi.info/feed/here/?token=382314e25caeccc6e05c242057bc022b04e38961')
data = json.loads(r.content)
data = data['data']
iaqi = data['iaqi']
forecast = data['forecast']
time = data['time']
pprint.pprint(time)


ref = db.reference("aqi")

ref.child(time['s']).push(iaqi)
ref.child(time['s']).push(forecast)