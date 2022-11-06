#! /usr/local/bin/python3

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, storage
import pandas as pd
import os
import socket
import threading
import _pickle as cPickle
import requests


# Student name: Cian Ó Gaora
# Student Number: 18323533

#firebase vairables
cred = credentials.Certificate(
    "weather-data-storage-c33f7-firebase-adminsdk-z15ho-415ecaf7dd.json")
app = firebase_admin.initialize_app(
    cred, {'databaseURL': 'https://weather-data-storage-c33f7-default-rtdb.europe-west1.firebasedatabase.app'})

PORT = 12345
HOST = "127.0.0.1"
count = 1


threads = []

#Function to upload a pd dataframe to the db
def upload_frame(frame):
    frame = frame.fillna('None')
    date = str(frame.index[0].date())
    time = str(frame.index[0])
    ref = db.reference("hourly-weather")
    postdata = frame.to_dict('records')

    ref.child(date).child(time).push(postdata)
    print(f'pushed data for {date}')


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print("server started")

conn, addr = s.accept()


with conn:
    print(f"Connected by {addr}")
    while True:
        # receive latest data from sensor
        data = conn.recv(2048)

        # check if data is command to stop receiving
        try:
            tmp = data.decode()
            if tmp == "done":
                print('finish command received!')
                for t in threads:
                    t.join()
                break

        except UnicodeDecodeError:
            pass

        # decode data to dataframe format
        data = cPickle.loads(data)
        print(data)
        # Start new thread to upload this dataframe
        thread = threading.Thread(target=upload_frame, args=(data,))
        threads.append(thread)
        thread.start()
        # upload_frame(data)

        # send recognition of reception
        conn.sendall(count.to_bytes(2, 'big'))
        count += 1

    print("Server shutting down")
