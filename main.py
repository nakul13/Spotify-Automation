import spotipy
import Login
import json
from spotipy.oauth2 import SpotifyOAuth
import pprint

# Get auth values from Login.py
SPOTIPY_CLIENT_ID = Login.SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET = Login.SPOTIPY_CLIENT_SECRET
SPOTIPY_REDIRECT_URI = Login.SPOTIPY_REDIRECT_URI

# Permissions needed - https://developer.spotify.com/documentation/general/guides/scopes/#user-modify-playback-state
scope = "user-read-playback-state user-modify-playback-state user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))

# Get user details and extract username
userDict = sp.current_user()
#print(json.dumps(userDict, sort_keys=True, indent=4))
userName = userDict["display_name"]

# Get a list of devices available
deviceDict = sp.devices()
#print(json.dumps(deviceDict, sort_keys=True, indent=4))

print("For user - " + userName + ", the following devices were found - ")

availableDeviceDict = {}
deviceCount = 1

for device in deviceDict["devices"]:
    devId = device["id"]
    devName = device["name"]
    devType = device["type"]
    devVolume = device["volume_percent"]
    
    availableDeviceDict[str(deviceCount)] = {"name":devName, "id":devId, "type":devType, "volume":devVolume}
    print("\t"+str(deviceCount) + " - " + devName)
    deviceCount = deviceCount + 1

playDevice = input("\nWhich device would you like to play on?\t")


# I have a dict of playlists in login.py to choose from
# preDefPlaylists = {
# "My playlist":"spotify:playlist:URI",
# }
# https://community.spotify.com/t5/Desktop-Windows/URI-Codes/td-p/4479486

whichPlaylists = input("Do you want to use the predefined list of playlists, or do you want to choose from the list of user playlists?\n\t0 - Use predefined list of playlists\n\t1 - Use user playlists\n")

to_play_playlistName = ""
to_play_playlistURI = ""

if whichPlaylists == "0":
    print("\nFollowing predefined playlists are available - ")
    
    playlistCount = 1
    preDef = {}

    for playlistName in Login.preDefPlaylists:
        preDef[str(playlistCount)] = playlistName
        print(str(playlistCount) + " - " + playlistName)
        playlistCount = playlistCount + 1

    playPlaylist = input("\nWhich playlist would you like to play?\t")

    if (int(playPlaylist) >= playlistCount) or (int(playPlaylist) < 1):
        print("Invalid selection")
        exit()

    to_play_playlistName = preDef[playPlaylist]
    to_play_playlistURI = Login.preDefPlaylists[to_play_playlistName]


elif whichPlaylists == "1":
    # Get user playlists
    playlistDict = sp.current_user_playlists(limit=20)
    #print(json.dumps(playlistDict, sort_keys=True, indent=4))

    print("\nUser - " + userName + " has the following playlists - ")

    userPlaylistDict = {}
    playlistCount = 1

    for playlist in playlistDict["items"]:
        playlistName = playlist["name"]
        playlistID = playlist["id"]
        playlistURI = playlist["uri"]

        userPlaylistDict[str(playlistCount)] = {"name": playlistName, "id":playlistID, "uri":playlistURI}
        print("\t" + str(playlistCount) + " - " + playlistName)
        playlistCount = playlistCount + 1

    playPlaylist = input("\nWhich playlist would you like to play?\t")

    if (int(playPlaylist) >= playlistCount) or (int(playPlaylist) < 1):
        print("Invalid selection")
        exit()

    to_play_playlistName = userPlaylistDict[playPlaylist]["name"]
    to_play_playlistURI = userPlaylistDict[playPlaylist]["uri"]


# Playlist tracks can be shuffled
shuffleOn = input ("\nDo you want the tracks shuffled?\n\t0 - Shuffle tracks\n\t1 - Do not shuffle tracks\n")

if shuffleOn == "0":
    sp.shuffle(True, availableDeviceDict[playDevice]["id"])
else:
    sp.shuffle(False, availableDeviceDict[playDevice]["id"])

 
# Begin playing the song

print("\nPlaying playlist '" + to_play_playlistName + "' on " + availableDeviceDict[playDevice]["name"] + "\n")

sp.start_playback(device_id=availableDeviceDict[playDevice]["id"], context_uri=to_play_playlistURI)
