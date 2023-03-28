"""---------------------------------------- Spotify Playlist Creator ----------------------------------------
In this code, a playlist creation program is written. First, the user is asked what year he is interested in music.
Then, by scripting the site https://www.billboard.com, the hot music of that year is identified.
Finally, using the Spotify API, the music playlist is created on this site.

* To use the spotify api, you need to register on this site and create an application in the developer dashboard
https://developer.spotify.com/dashboard

* To use the Spotify API, you can use the technical document https://spotipy.readthedocs.io/en/2.22.1/
"""

# ---------------------------------------- Add Required Library ----------------------------------------

import os

import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

# ---------------------------------------- Add Parameters ----------------------------------------

client_id = "SPOTIFY_CLIENT_ID"
client_secret = "SPOTIFY_CLIENT_SECRET"

# ---------------------------------------- Get Date ----------------------------------------

day = input("What day do you want to have top music? (YYY-MM-DD)\n")

# ---------------------------------------- Get Song Names ----------------------------------------

song_response = requests.get("https://www.billboard.com/charts/hot-100/" + day)
soup = BeautifulSoup(song_response.text, 'html.parser')
song_names_spans = soup.find_all("li", class_="lrv-u-width-100p")
song_title = [song.getText().split("\t") for song in song_names_spans]
song_names = []
for song in song_title:
    for i in range(0, len(song) - 1):
        if song[i] != '' and '\n' not in song[i]:
            song_names.append(song[i])

# ---------------------------------------- Spotify Authentication ----------------------------------------

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.getenv(client_id),
        client_secret=os.getenv(client_secret),
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

# ---------------------------------------- Playlist Creation ----------------------------------------

song_uris = []
year = day.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{day} Billboard 100",
    public=False
)
print(playlist)

sp.playlist_add_items(
    playlist_id=playlist["id"],
    items=song_uris
)
