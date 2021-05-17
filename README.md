# SpotifyQueueAdder
A personal project to integrate Spotify API with Google API

## Basic Functionality
The user will intitalize a Google Form which funnels responses to a Google Sheet. Utilizing the Google API, the user can fetch updates to the Google Sheet, take the newest song request, and send it to the Spotify API. The Spotify API will return the Track URI which can then be re-sent to the Spotify API to add to the User's Spotify now-playing Queue.



## Process for Initial Setup
  * Setup project with Google Cloud Developer
    * This grants access to Service Account/API Keys for Google
  * Setup project with Spotify Developers & set redirect URI (Set to https://github.com/ as default)
    * This grants access to Spotify API/keys
  * Setup Google Form & redirect responses to Google Sheet
    * Invite Google Cloud Developer project to Sheet
    * `playlist_loop` in `spotify_extract.py` currently assumes song request start in position **B2**
    * User must include a third column (**C**) for Status of each song, scripts will update the status directly
  * Update `spotify_keys.json` & `google_keys.json` with relevant API information
    * `google_keys.json` is renamed from file give directly from Google Cloud Developers

## Process for Normal Use
   * Get ID of Google Sheet, the bolded section of the URL:
     * *docs.google.com/spreadsheets/d/* **xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx** */edit?resourcekey#gid=?????????*
       * May update scripts to parse URL directly, haven't decided yet 
   * Make sure `*_keys.json` files are properly setup
   * Have music already running on an active device
     * The Spotify API cannot add to the queue if nothing is playing 
