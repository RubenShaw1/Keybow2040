import json
import serial
import time
# CHANGE SERIAL PORT IF NEEDED
ss = serial.Serial("COM4")

_ = ss.readline()

while True:
    raw_string = ss.readline().strip().decode()
    data = json.loads(raw_string)
    print(data)
    time.sleep(4)
