import json
import serial
import time
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from colorsys import hsv_to_rgb
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

devices = AudioUtilities.GetSpeakers()
load_dotenv()
SPOTIFY_CLIENT_ID=os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET=os.environ["SPOTIFY_CLIENT_SECRET"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri="http://localhost:8080/",
                                               scope="user-read-playback-state, user-library-read, user-library-modify", cache_path='./cache.txt'))

interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)





serial = serial.Serial("COM4")

def int_to_color(value):
    
    hue = (120 - (value * 1.2)) / 360.0 
    saturation = 1.0
    brightness = 1.0

    r, g, b = hsv_to_rgb(hue, saturation, brightness)

    return int(r * 255), int(g * 255), int(b * 255)


def is_current_song_liked():
    results = sp.current_user_saved_tracks()
    saved_tracks = [item['track']['id'] for item in results['items']]
    #print(saved_tracks)
    current_track_id = sp.current_playback()['item']['id']
    if current_track_id is None:
        return False
    #print(current_track_id)
    return current_track_id in saved_tracks


def like_current_song():
    current_track_id = sp.current_playback()['item']['id']
    print(current_track_id)
    sp.current_user_saved_tracks_add(tracks=[current_track_id])
    return True





while True:
    try:
        volume = interface.QueryInterface(IAudioEndpointVolume)
        muted = str(volume.GetMute())
        muted = eval(muted)
        playpause = int(True)
        volume_percent = round(volume.GetMasterVolumeLevelScalar()*100)
        volume_colour = str(int_to_color(volume_percent))
        volume_colour = volume_colour.strip("()")
        current_liked = is_current_song_liked()
        json_data = f'{{"toggle_mute": {int(muted)}, "toggle_playpause": {playpause}, "volume_percent": {volume_percent}, "current_liked": {int(current_liked)}}}'
        json_bytes = json_data.encode()

        
        to_write = json_bytes + "\n".encode()
        print(json_data)
        serial.write(to_write)
        #print("checkpoint 4")
        #print(muted, playpause, volume_colour)
        #print(muted)
        #print(int_to_color(volume_percent))
        time.sleep(5)
    except KeyboardInterrupt:
        break
