# Code Execution Instructions

### Running the Code
You will need your own api key stored in a text file called 'api_key.txt', located in the same directory as this project.
You will also need a json file containing credentials for a firebase realtime database. Any lines which access the database will need to be using this file for the `Cred` variable. You will also need to replace any lines with `{databaseURL: <url>` to your own database url.
Open two terminal windows and ensure that they are in the same directory as the source files.
In one terminal enter the following command:

`python3 firebase.py`

Server will display that it is running.
In the other terminal window, enter the follwing command:

`python3 sensor.py`

### Modifying the date range
The current code will upload real-time, hourly weather values from 01/01/2022 to 30/10/2022, with updates from every 4 hours.
The sensor.py file can be edited to change the date range of the readings by editing these lines: 

```python
start = datetime(2022, 1, 1)
end = datetime(2022, 10, 30)
```
### Choosing Hourly/Daily readings
Readings can be changed by altering line 31 in sensor.py and changing 'Hourly' to 'Daily', and changing line 40 from 
```python
start += timedelta(hours=4)
```
to
```python
start += timedelta(days=1)
```

Remember to also change 'firebase.py' to handle these changes.
The upload_thread must be changed to: 
```python
def upload_frame(frame):
    frame = frame.fillna('None')
    date = str(frame.index[0].date())
    time = str(frame.index[0])
    ref = db.reference("daily-avg-weather")
    postdata = frame.to_dict('records')

    ref.child(date).push(postdata)
    print(f'pushed data for {date}')
```

### Cleaning the Database
Run the script with the following command:

`python3 clean_db.py`

Enter the name of the node to be deleted