import json
import serial
import time
import random

# CHANGE SERIAL PORT IF NEEDED
serial = serial.Serial("COM4")

while True:
    try:
        key = random.randint(0, 15)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        colour = [r, g, b]

        # Prepare JSON strings for key and color
        key_json = json.dumps({"key": str(key)})
        colour_json = json.dumps({"colour": str(colour)})
        clear_json = json.dumps({"clear": "1"})

        # Send JSON strings over serial
        serial.write((key_json + "\n").encode())
        serial.write((colour_json + "\n").encode())
        serial.write((clear_json + "\n").encode())
        time.sleep(3)
    except KeyboardInterrupt:
        break
