import spotipy 
import json 

def connect_to_spotify():
    credentials = json.load(open("spotify_credentials.json"))

    token = spotipy.util.prompt_for_user_token(
        username="trumpeter96",
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        redirect_uri=credentials["redirect_uri"]
        )

    credentials["code"] = token

    with open("spotify_credentials.json", 'w') as f:
        json.dump(credentials, f)

    sp = spotipy.Spotify(auth=token)
    return sp 
