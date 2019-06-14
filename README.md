# Spaubot
**A bot for managing your Spotify playlists, via Matrix!**
(*written in Python 3.7.3*)
## Setup
There are several steps you will need to take in order to work on development of this bot. 

1. Clone this repository
2. (Optional **Highly Recommended**) Set-up a Python 3 virtual environment 

    `python3 -m venv [path]`

3. Install the dependencies: 

    ```shell
    pip install matrix_client
    pip install pyyaml
    pip install git+https://github.com/plamere/spotipy.git
    ```

4. Fill out the config.yaml file. The matrix information is specific to the matrix server you are using. The matrix room can be found by going to the advanced settings in the chat application (Riot). The spotify client id and secret can be obtained by registering an app at https://developer.spotify.com/

    ```
    matrix_host: "https://matrix.org"
    matrix_username: ""
    matrix_password: ""
    matrix_room: ""
    spot_username: ""
    spot_client_id: ""
    spot_client_secret: "" 
    spot_playlist_id: ""
    spot_redirect_uri: "http://localhost/"
    ```

5. Run the spaubot.py script locally to obtain your authorization token. This will open up a web browser and direct you to login to Spotify. This must be done anytime you alter the access scope within the script--Otherwise a refresh token will be saved in a dotfile. 



## Usage
The original intended usage of this bot was to automate playlist additions  suggested by a collaborative group. This eliminates the need to become a Spotify user in order to add song suggestions to a playlist.

The bot can be prompted by a series of chat commands.

  * `!Add [ArtistName] - [SongName]` => This will search the Spotify API for the best match and add this song to the current playlist. If no results are found, the bot will notify the chat.

  * `!Current`  => Returns the song that is currently playing.
  
## To Be Added


#### References
1. https://github.com/matrix-org/matrix-python-sdk.git
2. https://github.com/plamere/spotipy