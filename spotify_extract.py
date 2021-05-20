from time import sleep
import sys
from google_API import FormReader
from spotify_API import SpotAdder
from queue import *
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

def begin(song_comms):    
    '''
    Check desired use mode
    -sys.argv[1] == 'Debug': shortens sleep timer for quicker scans of Google Sheet
                             otherwise set timer to normal 30 seconds
    '''
    global SLEEP_TIME

    try:
        debug_check = song_comms.get_nowait()
        if debug_check == 'Set DEBUG':
            SLEEP_TIME = 5
    except Empty:
        pass

    #Initalize FormReader
    song_comms.put('ID')
    while not song_comms.empty():
        pass
    
    while True:
        try:
            sheet_ID = song_comms.get_nowait()
            break
        except Empty:
            pass
    song_form = prepare_read(sheet_ID)
    
    #Initalize SpotAdder
    spot_queue = SpotAdder()
    
    print(sheet_ID)
    #Loop for song requests
    #playlist_loop(song_form, spot_queue)
