import usb_cdc
import time
from pmk import PMK
from pmk.platform.keybow2040 import Keybow2040 as Hardware
import json

keybow = PMK(Hardware())
keys = keybow.keys

while True:
    keybow.update()
    if usb_cdc.data.in_waiting:
        received_data = usb_cdc.data.readline().decode().strip()
        #print("Received data:", received_data)
        
        try:
            json_data = json.loads(received_data)
            if "key" in json_data:
                key_data = json_data["key"]
                key = int(key_data)
            elif "colour" in json_data:
                colour_data = json_data["colour"]
            elif "clear" in json_data:
                clear = json_data["clear"]
                clear = int(clear)
    
                #print(colour_data)

                rgb_values = colour_data.strip('[]').split(',')
                r, g, b = map(int, rgb_values)

                #print("R:", r, "G:", g, "B:", b)

                keys[key].set_led(r, g, b)
                #print("LED set")
                
                if clear == 1:
                    for key_num in range(16):
                        keys[key_num].set_led(0, 0, 0)
                else:
                    continue
    
        except ValueError as e:
            print("JSON decode error:", e)
            
        except KeyboardInterrupt:
            keybow.set_all(0,0,0)
            break
        
        except keybow.any_pressed:
            break
        
            
