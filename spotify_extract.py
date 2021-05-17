from time import sleep
import sys
from google_API import FormReader
from spotify_API import SpotAdder
import re

SLEEP_TIME = 30

def prepare_read(sheet_ID):
    song_form = FormReader(sheet_ID)
    song_form.start_service()
    
    return(song_form)

def playlist_loop(song_form, spot_queue):
    #Check if there is an active device before continuing
    spot_queue.check_devices()
    
    #Check where to start in sheet
    spot_queue.check_start(song_form)
    if spot_queue.song_ind > 2:
        print('\nStarting after song {}\n'.format(spot_queue.song_ind - 1))
    else:
        print('\nStarting at the top!\n')
    
    #Loop and scan for song requets
    while True:
        #Sleep so sheet isn't scanned contiually
        sleep(SLEEP_TIME)
        
        #Check if new song requested
        req_song = song_form.get_range(FormReader.RANGE_BASE + 'B' + str(spot_queue.song_ind))[0][0]
        
        if req_song == 'No new value':
            print('No new song requests')
        else:
            #Some regex to replace 'By' with '-', Spotify struggles with 'By' for some reason
            song = re.sub(f'( [Bb][Yy] )', ' - ', req_song)
            spot_queue.add_queue(song, song_form)
            spot_queue.song_ind += 1

if __name__ == "__main__":
    
    '''
    Check desired use mode
    -sys.argv[1] == 'Debug': shortens sleep timer for quicker scans of Google Sheet
                             otherwise set timer to normal 30 seconds
    '''
    if len(sys.argv) > 1:
        SLEEP_TIME = 5 if sys.argv[1] == 'Debug' else 30
        print('\nSleep time between sheet scans: {} seconds'.format(SLEEP_TIME))
        
    #Initalize FormReader
    sheet_ID = input("\nInput google sheet ID: ")
    song_form = prepare_read(sheet_ID)
    
    #Initalize SpotAdder
    spot_queue = SpotAdder()
    
    #Loop for song requests
    playlist_loop(song_form, spot_queue)
