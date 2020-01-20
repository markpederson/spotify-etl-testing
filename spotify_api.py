import spotify_auth
import numpy as np 
import json
import pandas as pd
import datetime 
import sys

spotify_credentials_path = "spotify_credentials.json"
sp = spotify_auth.connect_to_spotify()

# test = sp.artist_albums(artist_id="2aqFBHOpM9uIgBpUsdq09x")

def get_new_artist(spotify_credentials_path):
    spotify_credentials = json.load(open(spotify_credentials_path))
    related_artists = sp.artist_related_artists(spotify_credentials["last_artist"])["artists"]
    rand_int = np.random.randint(0, len(related_artists))
    new_id = related_artists[rand_int]["id"]
    spotify_credentials["last_artist"] = new_id
    with open(spotify_credentials_path, 'w') as f:
        json.dump(spotify_credentials, f)
    return new_id

new_artist_id = get_new_artist(spotify_credentials_path)
new_artist_albums = sp.artist_albums(artist_id=new_artist_id)

tracks_data = []

for item in new_artist_albums["items"]:
    al = sp.album(item["id"])
    for track in al["tracks"]["items"]:
        trk = sp.track(track["id"])
        trk_data = [
            trk["album"]["name"],
            ", ".join([a["name"] for a in trk["artists"]]),
            ", ".join(m for m in trk["available_markets"]),
            trk["disc_number"],
            trk["duration_ms"],
            trk["explicit"],
            trk["href"],
            trk["id"], 
            trk["is_local"], 
            trk["name"], 
            trk["popularity"], 
            trk["track_number"],
            trk["uri"]
        ]
        tracks_data.append(trk_data)

tracks_df = pd.DataFrame(data=tracks_data, columns=[
    "album_name",
    "artists",
    "available_markets",
    "disc_number",
    "duration_ms",
    "explicit",
    "href",
    "id",
    "is_local",
    "name",
    "popularity",
    "track_number",
    "uri"
])

tracks_df['last_updated'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

tracks_df.to_csv("files/tracks_df.csv", index=False)