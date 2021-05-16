import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

class SpotAdder:
    SPOT_API_KEYS = 'keys.json'
    SPOT_API_REDIRECT_URI = 'https://github.com/'
    SPOT_API_SCOPE = 'user-modify-playback-state user-read-playback-state'
    
    def __init__(self):
        self.key_read()
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.CLIENT_ID,
                                                            client_secret=self.CLIENT_SECRET,
                                                            redirect_uri=SpotAdder.SPOT_API_REDIRECT_URI,
                                                            scope=SpotAdder.SPOT_API_SCOPE))
    
    def key_read(self):
        with open(SpotAdder.SPOT_API_KEYS) as f:
            keys = json.load(f)
        self.CLIENT_ID = keys['client_id']
        self.CLIENT_SECRET = keys['client_secret']
    
    def add_queue(self, song):
        song_data = self.sp.search(q=song, type='track', limit=1)
        song_uri = song_data['tracks']['items'][0]['uri']
        print(song + ': ' + song_uri)
        self.sp.add_to_queue(uri=song_uri)
    
    def check_devices(self):
        if self.sp.devices()['devices'] == []:
            raise SystemExit("\nNo active devices on Spotify account. \nPlease start playing music on account to allow proper addition of songs to queue.")
        else:
            print("Active device detected, continuing")