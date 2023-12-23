import usb_cdc
import time
from pmk import PMK
from pmk.platform.keybow2040 import Keybow2040 as Hardware
import random

keybow = PMK(Hardware())
keys = keybow.keys
serial = usb_cdc.data

while True:
    num = random.randint(0, 1000)
    data_to_send = f'{{"number": "{num}"}}\n'
    usb_cdc.data.write(data_to_send.encode())
    keys[1].set_led(255,0,0)
    time.sleep(2)
    keys[1].set_led(0,255,0)
    time.sleep(2)
