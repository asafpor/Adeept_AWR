# Import libraries
import os
import sys
import json
import spotipy
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import spotipy.util as util
from json.decoder import JSONDecodeError

if __name__ == '__main__':
    # Get the username from terminal
    username = sys.argv[1]
    scope = 'user-read-private user-read-playback-state user-modify-playback-state'

    try:
        token = util.prompt_for_user_token(username, scope)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope)

    # create a client authentication request
    #client_cred = SpotifyClientCredentials(
    #    client_id="27edd4a6dfd845c5a61347337b3c7ce6",
    #    client_secret="478717682ad44846a51aa4faa7e1dafe"
    #)
    # Create Spotify object
    #birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
    #spotifyObject = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    #results = spotifyObject.artist_albums(birdy_uri, album_type='album')
    
    # Create Spotify object
    spotifyObject = spotipy.Spotify(auth=token)
    devices = spotifyObject.devices()
    print(json.dumps(devices, sort_keys=True, indent=4))
    deviceID = devices['devices'][0]['id']
    #print(results)

    quit()

    # Get track information
    track = spotifyObject.current_user_playing_track()
    print(json.dumps(track, sort_keys=True, indent=4))
    print()
    artist = track['item']['artists'][0]['name']
    track = track['item']['name']

    if artist !="":
        print("Currently playing " + artist + " - " + track)


    # User information
    user = spotifyObject.current_user()
    displayName = user['display_name']
    follower = user['followers']['total']


    while True:

        print()
        print(">>> Welcome to Spotify " + displayName + " :)")
        print(">>> You have " + str(follower) + " followers.")
        print()
        print("0 - Search for an artist")
        print("1 - exit")
        print()

        choice = input("Enter your choice: ")
        # End program
        if choice == "1":
            break
        # Search for artist    
        elif choice == "0":
            print()
            searchQuery = input("Ok, what's their name?:")
            print()
            # Get search results
            searchResults = spotifyObject.search(searchQuery,1,0,"artist")
            # Print artist details
            artist = searchResults['artists']['items'][0]
            print(artist['name'])
            print(str(artist['followers']['total']) + " followers")
            print(artist['genres'][0])
            print()
            webbrowser.open(artist['images'][0]['url'])
            artistID = artist['id']
            # Album details
            trackURIs = []
            trackArt = []
            z = 0

            # Extract data from album
            albumResults = spotifyObject.artist_albums(artistID)
            albumResults = albumResults['items']

            for item in albumResults:
                print("ALBUM: " + item['name'])
                albumID = item['id']
                albumArt = item['images'][0]['url']

                # Extract track data
                trackResults = spotifyObject.album_tracks(albumID)
                trackResults = trackResults['items']

                for item in trackResults:
                    print(str(z) + ": " + item['name'])
                    trackURIs.append(item['uri'])
                    trackArt.append(albumArt)
                    z+=1
                print()

                # See album art
            while True:
                songSelection = input("Enter a song number to see the album art: ")
                if songSelection == "x":
                    break
                trackSelectionList = []
                trackSelectionList.append(trackURIs[int(songSelection)])
                spotifyObject.start_playback(deviceID, None, trackSelectionList)
                webbrowser.open(trackArt[int(songSelection)])


