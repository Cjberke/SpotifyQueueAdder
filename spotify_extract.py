# importing the required libraries
from time import sleep
from google_API import FormReader
from spotify_API import SpotAdder
import re

def prepare_read(sheet_ID):
    song_form = FormReader(sheet_ID)
    song_form.start_service()
    
    return(song_form)

def playlist_loop(song_form, spot_queue):
    #i == 1: column title
    #i == 2: first song request
    i = 54
    while True:
        #Sleep so sheet isn't scanned contiually
        sleep(5)
        
        #Check if new song requested
        song = song_form.get_range(FormReader.RANGE_BASE + 'B' + str(i))[0][0]
        
        if song == 'No new value':
            print('No new song requests')
        else:
            song = re.sub(f'( [Bb][Yy] )', ' - ', song)
            print(song)
            i += 1

def add_queue(song, sp):
    song_data = sp.search(q=song, type='track', limit=1)
    uri = song_data['tracks']['items'][0]['uri']
    print(uri)
    results = sp.add_to_queue(uri=uri)
    return

if __name__ == "__main__":
    
    #Initalize FormReader
    sheet_ID = input("Input google sheet ID: ")
    song_form = prepare_read(sheet_ID)
    
    #Initalize SpotAdder
    spot_queue = SpotAdder()
    
    #Loop for song requests
    playlist_loop(song_form, spot_queue)
