import random
import threading
import pandas as pd
from pathlib import Path
from pynput import keyboard
from datetime import datetime

run_collect = False
index = 0.0
mutex = threading.Lock()
#----- Monitoring the keyboard begin -------
def on_press(key):
    global mutex, run_collect
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))            
    except AttributeError:
        # print('special key {0} pressed'.format(key))
        if key == keyboard.Key.esc:
            keyboard.Listener.stop()
            print('Stop keyboard.Listener')
        elif key == keyboard.Key.space:
            mutex.acquire()
            run_collect = True
            mutex.release()

def on_release(key):
    global mutex, run_collect, index
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    if key == keyboard.Key.space:
        mutex.acquire()
        run_collect = False
        index += 1.0
        mutex.release()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
#----- Monitoring the keyboard end -------

ServerURL = 'https://2.iottalk.tw' #For example: 'https://iottalk.tw'
MQTT_broker = None # MQTT Broker address, for example:  'iottalk.tw' or None = no MQTT support
MQTT_port = 5566
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'Dummy_Device'
IDF_list = ['Dummy_Sensor']
ODF_list = ['Dummy_Control']
device_id = None #if None, device_id = MAC address
device_name = 'testinlab403'
exec_interval = 0.1  # IDF/ODF interval

def on_register(r):
    print('Server: {}\nDevice name: {}\nRegister successfully.'.format(r['server'], r['d_name']))

def Dummy_Sensor():
    return random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100) 

def Dummy_Control(data:list):
    collect_data = data
    if run_collect:
        collecting_data(collect_data)


collected_df = pd.DataFrame(columns=['num', 'timestamp', 'acc1','acc2','acc3','gyro1','gyro2','gyro3','orien1','orien2','orien3'])
def collecting_data(data:list):
    global collected_df, index
    num = index
    collect = {
        'num': num,
        'timestamp': str(datetime.utcnow()),
        'acc1': data[0][0],
        'acc2': data[0][1],
        'acc3': data[0][2],
        'gyro1': data[0][3],
        'gyro2': data[0][4],
        'gyro3': data[0][5],
        'orien1': data[0][6],
        'orien2': data[0][7],
        'orien3': data[0][8]}
    collected_df.loc[len(collected_df.index)] = collect
    print('{}: {}'.format(len(collected_df.index), collect))    
    return 0


def store_dataframe():
    global collected_df
    filepath = Path('./other.csv')
    print('\nSave', str(filepath))
    collected_df.to_csv(filepath, index=False)
