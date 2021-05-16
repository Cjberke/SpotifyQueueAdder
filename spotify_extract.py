# importing the required libraries
from time import sleep, time
from google_API import FormReader
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

SPOT_API_KEYS = 'keys.json'

def prepare_read(sheet_ID):
    song_form = FormReader(sheet_ID)
    song_form.start_service()
    
    return(song_form)

def spot_read():
    with open(SPOT_API_KEYS) as f:
        keys = json.load(f)
    CLIENT_ID = keys['client_id']
    CLIENT_SECRET = keys['client_secret']
    return CLIENT_ID, CLIENT_SECRET

def playlist_loop(client, sp):
    i = 0
    while True:
        #Sleep for 10 seconds so we don't contiually scan sheet
        sleep(5)
        #Get the instance of the Spreadsheet
        sheet = client.open('PythonSongRequests')
        #Get the first sheet of the Spreadsheet
        sheet_instance = sheet.get_worksheet(0)
        #Get all the records of the data
        records_data = sheet_instance.get_all_records()

        #Read next line of sheet
        try:
            #If new song requested, try to see what it is
            song = records_data[i]['What song would you like to hear?']
            song = re.sub(f'( [Bb][Yy] )', ' - ', song)
            print(song)
            i += 1
            add_queue(song, sp)
            continue
            #If no new song, catch exception and continue through loop
        except IndexError:
            print("No new value")
            pass

def add_queue(song, sp):
    song_data = sp.search(q=song, type='track', limit=1)
    uri = song_data['tracks']['items'][0]['uri']
    print(uri)
    results = sp.add_to_queue(uri=uri)
    return

if __name__ == "__main__":
    #Initalize google sheet to read from
    sheet_ID = input("Input google sheet ID: ")
    song_form = prepare_read(sheet_ID)
    CLIENT_ID, CLIENT_SECRET = spot_read()
    #Loop through requests ad infinitum
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri="https://github.com/",
                                                scope="user-modify-playback-state"))
    #playlist_loop(sheet, sp)
