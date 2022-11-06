#! /usr/local/bin/python3

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, storage


cred = credentials.Certificate("weather-data-storage-c33f7-firebase-adminsdk-z15ho-415ecaf7dd.json")
app  = firebase_admin.initialize_app(cred, {'databaseURL':'https://weather-data-storage-c33f7-default-rtdb.europe-west1.firebasedatabase.app'})

node = str(input("Enter the name of the node to remove: "))

ref = db.reference(node)

ref.delete()