# Error Codes:
# 1 - Unknown problem has occured
# 2 - Could not find the server.
# 3 - Bad URL Format.
# 4 - Bad username/password.
# 11 - Wrong room format.
# 12 - Couldn't find room.

##########################################
#           To be implemented            
# - Displayer user's bot-created playlists
# - Allow user to create new playlist
# - Allow user to cancel last song addition
# - Display user commands
# - Squanch.
# - Functionize
##########################################
# Finding data when searching by track
# sp.search(search_string, type='track')
#
# artist:           results['tracks']['items'][0]['album']['artists'][0]['name'] #artist
# album:            results['tracks']['items'][0]['album']['name'] #album
# track_name:       results['tracks']['items'][0]['name'] #track name
# uri:              results['tracks']['items'][0]['uri'] #uri
# id:               results['tracks']['items'][0]['id'] #id
#
# --iterate through results -- 
# for item in results['tracks']['items']:
#     print(f"{item['album']['artists'][0]['name']} - {item['name']}")


import sys
import console_input 
import logging
import spotipy
import spotipy.util as util
import yaml

from matrix_client.client import MatrixClient
from matrix_client.api import MatrixRequestError
from requests.exceptions import MissingSchema


# Called when a message is recieved.
def load_config():
    global user_config
    stream = open('config.yaml')
    user_config = yaml.safe_load(stream)


def on_message(room, event):
    if event['type'] == "m.room.member":
        if event['membership'] == "join":
            print("{0} joined".format(event['content']['displayname']))
    elif event['type'] == "m.room.message":
        if event['content']['msgtype'] == "m.text":
            msg = event['content']['body']
            sender = event['sender']
            print("{0}: {1}".format(sender, msg))
            if msg[0] == '!':
                cmd = msg.split(' ')[0].lower()
                if cmd == "!help":
                    room.send_text("Here's a list of commands!") #needs implemented
                elif cmd == "!add":
                    print("You want to add a track!")
                    if len(msg) > 5:
                        results = sp.search(msg[5:], type='track')
                        if results['tracks']['items']:
                            track_ids = []
                            track_ids.append(results['tracks']['items'][0]['id'])
                            try:
                                tracks_added = sp.user_playlist_add_tracks(user_config['spot_username'], user_config['spot_playlist_id'], track_ids)
                                room.send_text(f"{results['tracks']['items'][0]['album']['artists'][0]['name']} - {results['tracks']['items'][0]['name']} added to the playlist!")
                            except:
                                room.send_text(f"{sender} Unable to add {msg}!") 
                        else:
                            room.send_text(f"{sender} There were no results for '{msg[5:]}'. Please verify the spelling is correct.")
                    else:
                        room.send_text(f"'{msg}' is not a valid command. Please use the format `!add [Artist] - [Song]`")
                elif cmd == "!cancel":
                    print("You want to cancel the last added track?")#TO BE IMPLEMENTED
                elif cmd == "!current":
                    print("You want the current track?")
                    current_track = sp.currently_playing()
                    if current_track:
                        room.send_text(f"Currently spinning {current_track['item']['artists'][0]['name']} - {current_track['item']['name']}")
                    else:
                        room.send_text(f"{sender} -- No songs are currently playing. Queue up a song with !add [artist] - [track]")
                elif cmd == "!switch":
                    print("You want to switch playlists?") #TO BE IMPLEMENTED
                elif cmd == "!playlist":
                    print("You want a list of songs on the current playlist?") #TO BE IMPLEMENTED
            elif msg[0] == '$':
                room.send_text("You've got my attentions.")
                results = sp.search(msg[1:], type='track')
                if results['tracks']['items']:
                    track_ids = []
                    track_ids.append(results['tracks']['items'][0]['id'])
                    try:
                        tracks_added = sp.user_playlist_add_tracks(user_config['spot_username'], user_config['spot_playlist_id'], track_ids)
                        room.send_text(f"{results['tracks']['items'][0]['name']} added to the playlist!")
                    except:
                        room.send_text(f"{sender} Unable to add {msg[1:]}!") 
                else:
                    room.send_text(f"{sender} There were no results for {msg[1:]}. Please verify the spelling is correct.")
    else:
        print(event['type'])

def spotify_login():
    scope = 'playlist-modify-public user-read-currently-playing'
    token = util.prompt_for_user_token(user_config['spot_username'],scope,user_config['spot_client_id'],user_config['spot_client_secret'],user_config['spot_redirect_uri'])

    if token:
        global sp 
        sp = spotipy.Spotify(auth=token)
    else:
        print ("Can't get token for", user_config['spot_username'])


def main(host, username, password, room_id_alias):
    client = MatrixClient(host)
    
    try:
        client.login_with_password(username, password)
    except MatrixRequestError as e:
        print(e)
        if e.code == 403:
            print("Bad username or password.")
            sys.exit(4)
        else:
            print("Check your server details are correct.")
            sys.exit(2)
    except MissingSchema as e:
        print("Bad URL format.")
        print(e)
        sys.exit(3)

    try:
        room = client.join_room(room_id_alias)
    except MatrixRequestError as e:
        print(e)
        if e.code == 400:
            print("Room ID/Alias in the wrong format")
            sys.exit(11)
        else:
            print("Couldn't find room.")
            sys.exit(12)

    room.add_listener(on_message)
    client.start_listener_thread()

    while True:
        msg = console_input.get_input()
        if msg == "/quit":
            break
        else:
            room.send_text(msg)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    global user_config
    bot_commands = {"AddSong" : "Adds a song to the current playist.", "CurrentPlaylist" : "Displays the current playlist."}
    load_config()
    spotify_login()

    
    print(f"Logging into {user_config['matrix_host']}")
    main(user_config['matrix_host'], user_config['matrix_username'], user_config['matrix_password'], user_config['matrix_room'])