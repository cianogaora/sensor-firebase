#! /usr/local/bin/python3
import socket
from datetime import datetime, timedelta
from meteostat import Point, Daily, units, Hourly
import _pickle as cPickle

# Student name: Cian Ó Gaora
# Student Number: 18323533

HOST = "127.0.0.1"
PORT = 12345

# Define time period of data collection
start = datetime(2022, 1, 1)
end = datetime(2022, 10, 30)


# latitude and longitude of Dublin
location = Point(53.3498, -6.2603)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # establish connection to server
    s.connect((HOST, PORT))

    # Command to be sent upon completion of transmission
    done_str = "done"
    while start != end:
        # Get hourly reading and convert to bytes format
        wdata = Hourly(location, start, start)
        wdata = wdata.fetch()
        df_bytes = cPickle.dumps(wdata)

        # Send data and receive response from server
        s.sendall(df_bytes)
        data = s.recv(2048)

        # Increment time of reading
        start += timedelta(hours=4)
        print(f"Received {data!r}")

    # Send command to end connection
    s.send(done_str.encode())