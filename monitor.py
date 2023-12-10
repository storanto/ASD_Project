import requests
from datetime import datetime
from collections import defaultdict
import sqlite3
import time
import numpy as np
import keyboard

def fetchdata(url):
    res = requests.get(url)
    data = res.json()
    print(data)
    return data

def check_values(data):
    faults = 0
    date = datetime.now()
    date = date.strftime("%d.%m.%Y %H:%M:%S")

    # Define your thresholds
    power_output_threshold = 2000
    power_output_lower_threshold = 500
    radiation_level_threshold = 100
    usage_capacity_percentage_threshold = 99
    usage_capacity_percentage_lower_threshold = 25
    
    if data['state'] == False: 
        print(f"<<Alert: POWER PLANT APPEARS TO BE OFFLINE (ONSTATE): {data['state'],date}>>") #state
        faults += 1

    if data['power_output'] > power_output_threshold or data['power_output'] < power_output_lower_threshold: #ouput%
        print(f"<<Alert: Power output is abnormal: {data['power_output'],date}>>")
        faults += 1
        
    if data['radiation_level'] > radiation_level_threshold:                          
        print(f"<<Alert: Radiation level is too high: {data['radiation_level'],date}>>") #radiation
        faults += 1
    
    if  data['usage_capacity_percentage'] < usage_capacity_percentage_lower_threshold or data['usage_capacity_percentage'] > usage_capacity_percentage_threshold : #usage
        print(f"Alert: <<Usage capacity percentage is abnormal: {data['usage_capacity_percentage'],date}>>")
        print(type(data['usage_capacity_percentage']))
        faults += 1
        
    if (faults > 0):
        print(f"{faults} Possible fault(s) detected!")
    else: 
        print("All systems seem to be working as expected!")

def main_loop():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PowerPlantLogs
    (timestamp text PRIMARY KEY, power_output int, radiation_level int, state BOOL, usage_capacity_percentage int)
''')
    while True:
        start_time = time.time()

        date = datetime.now()
        datekey = date.strftime("%d.%m.%Y %H:%M:%S")
        
        data = fetchdata('http://localhost:5000/random')

        check_values(data)

        cursor.execute("INSERT INTO PowerPlantLogs VALUES (?,?,?,?,?)", 
                  (datekey, data['power_output'], data['radiation_level'], data['state'], data['usage_capacity_percentage']))

        conn.commit()
        print("fetched some data")        
        end_time = time.time()
        
        #Ensure data is fetched every 60 seconds
        elapsed_time = end_time - start_time
        time_to_sleep = max(60 - elapsed_time, 0)

        time.sleep(time_to_sleep)

        
        if keyboard.is_pressed('ctrl+c'):
            print("Ctrl+C pressed. Exiting the loop.")
            break
    conn.close()
      
if __name__ == "__main__":
    main_loop()

    