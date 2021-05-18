import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

class SpotAdder:
    SPOT_API_KEYS = 'spotify_keys.json'
    SPOT_API_REDIRECT_URI = 'https://github.com/'
    SPOT_API_SCOPE = 'user-modify-playback-state user-read-playback-state'
    
    def __init__(self, playlist=None):
        self.key_read()
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.CLIENT_ID,
                                                            client_secret=self.CLIENT_SECRET,
                                                            redirect_uri=SpotAdder.SPOT_API_REDIRECT_URI,
                                                            scope=SpotAdder.SPOT_API_SCOPE))
        self.song_ind = 2
        self.playlist = playlist
    
    def key_read(self):
        with open(SpotAdder.SPOT_API_KEYS) as f:
            keys = json.load(f)
        self.CLIENT_ID = keys['client_id']
        self.CLIENT_SECRET = keys['client_secret']
    
    def add_queue(self, song, song_form):
        song_data = self.sp.search(q=song, type='track', limit=1)
        status = ''
        
        try:
            song_uri = song_data['tracks']['items'][0]['uri']
            print('\n' + song + ':  ' + song_uri)
            self.sp.add_to_queue(uri=song_uri)
            status = 'Added'
        
        except IndexError:
            print("\nCouldn't find song '{}', skipping".format(song))
            status = 'Skipped'
        self.check_song(song_form, status)
    
    def add_playlist(self, song_form, status):
        #TODO: Add option to build into playlist instead of Queue
        pass
    
    def check_song(self, song_form, status):
        song_ind_check = 'C' + str(self.song_ind)
        song_form.write_range(song_ind_check, [[status]])
         
    def check_devices(self):
        if self.sp.devices()['devices'] == []:
            raise SystemExit("\nNo active devices on Spotify account. \nPlease start playing music on account to allow proper addition of songs to queue.")
        else:
            print("\nActive device detected, continuing\n")
            
    def check_start(self, song_form):
        while True:
            status = song_form.get_range(song_form.RANGE_BASE + 'C' + str(self.song_ind))[0][0]
            if status == 'Added' or status == 'Skipped':
                self.song_ind += 1
            else:
                break