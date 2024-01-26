import usb_cdc
import time
from pmk import PMK, number_to_xy, hsv_to_rgb
from pmk.platform.keybow2040 import Keybow2040 as Hardware
import math
import json
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Setup
keybow = PMK(Hardware())
keys = keybow.keys
cc = ConsumerControl(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)


# Colours:
toggle_true_colour = 0,255,0 # Green default
toggle_false_colour = 255,0,0 # Red default
rainbow = False
step = 0
#
debounce = 0.09
fired = False

def int_to_colour(value):
    
    hue = (120 - (value * 1.2)) / 360.0 
    saturation = 1.0
    brightness = 1.0

    r, g, b = hsv_to_rgb(hue, saturation, brightness)

    return int(r), int(g), int(b)


notused = 2,3,5,6,7,9,10,11,12,14,15


while True: 
    keybow.update()
    if rainbow == False:
        for i in notused: keys[i].set_led(0,0,0)
        if usb_cdc.data.in_waiting:
            received_data = usb_cdc.data.readline().decode().strip()

            try:
                #print("Received data:", received_data)
                data = json.loads(received_data)
                print("Parsed data:", data)
                if "toggle_mute" in data:
                    toggle_mute = int(data['toggle_mute'])
                    print(toggle_mute)
                    if toggle_mute == 0:
                        keys[0].set_led(0,255,0)
                    elif toggle_mute == 1:
                        keys[0].set_led(255,0,0)

                if "toggle_playpause" in data:
                    toggle_playpause = int(data['toggle_playpause'])
                    if toggle_playpause == 1:
                        keys[1].set_led(0,255,0)
                    elif toggle_playpause == 0:
                        keys[1].set_led(255,0,0)
                
                if "volume_percent" in data:
                    volume_percent = int(data['volume_percent'])
                    volume_colour = int_to_colour(volume_percent)
                    print(volume_colour)
                    keys[4].set_led(*volume_colour)
                    keys[8].set_led(*volume_colour)

                if "current_liked" in data:
                    current_liked = int(data['current_liked'])
                    if current_liked == 1:
                        keys[13].set_led(0,255,0)
                    elif current_liked == 0:
                        keys[13].set_led(255,0,0)

            
            except ValueError as e:
                print("Parsed data before error:", data)
                print("JSON decode error:", e)
                print("Received data:", received_data)
    
    if keys[0].pressed:    
        if not fired:
            fired = True
            cc.press(ConsumerControlCode.MUTE)
            cc.release()
            
    if keys[1].pressed:
        if not fired:
            fired = True
            cc.press(ConsumerControlCode.PLAY_PAUSE)
            cc.release()
            
    if keys[2].pressed:
        if not fired: # Led strip on
            fired = True
            keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.K)

    if keys[3].pressed:
        if not fired:
            fired = True
            keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.ONE)
    
    if keys[4].pressed:
        if not fired:
            fired = True
            cc.press(ConsumerControlCode.VOLUME_DECREMENT)
            cc.release()
            
    
    if keys[5].pressed:
        if not fired:
            fired = True
            cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK) 
    
    if keys[6].pressed:
        if not fired: # Led strip off
            fired = True
            keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.K)
    
    if keys[7].pressed:
        if not fired:
            fired = True
            keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.TWO)
    
    if keys[8].pressed:
        if not fired:
            fired = True
            cc.press(ConsumerControlCode.VOLUME_INCREMENT)
            cc.release()
    
    if keys[9].pressed:
        if not fired:
            fired = True
            cc.press(ConsumerControlCode.SCAN_NEXT_TRACK)
            cc.release()
    
    if keys[10].pressed:
        pass # LED toggle
    
    if keys[11].pressed:
        if not fired:
            fired = True
            keyboard.send(Keycode.CONTROL, Keycode.ALT, Keycode.THREE)
    
    if keys[12].pressed:
        if not fired:
            fired = True
            keyboard.send(Keycode.GUI, Keycode.CONTROL, Keycode.V)
    
    if keys[13].pressed:
        pass # Spotify like/dislike current song 
    
    if keys[14].pressed: # Rainbow toggle
        if not fired:
            fired = True
            
            if rainbow == False:
                rainbow = True
            elif rainbow == True:
                rainbow = False
    
    if keys[15].held:
        if not fired:
            fired = True
            keyboard.send(Keycode.ALT, Keycode.F4)    

    if fired and time.monotonic() - keybow.time_of_last_press > debounce:
        fired = False

    elif rainbow == True:
        step += 1

        for i in range(16):
            # Convert the key number to an x/y coordinate to calculate the hue
            # in a matrix style-y.
            x, y = number_to_xy(i)

            # Calculate the hue.
            hue = (x + y + (step / 20)) / 8
            hue = hue - int(hue)
            hue = hue - math.floor(hue)

            # Convert the hue to RGB values.
            r, g, b = hsv_to_rgb(hue, 1, 1)

            # Display it on the key!
            keys[i].set_led(r, g, b)

