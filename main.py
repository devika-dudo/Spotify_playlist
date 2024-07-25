import spotipy
from an import get_100_songs
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

date = input("Which year do you want to get transported to? Type the date in this format YYYY-MM-DD: ")

load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
print(SPOTIPY_CLIENT_ID)

scope = "user-library-read playlist-modify-public playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])
user_id=sp.current_user()['id']

hundred_songs=get_100_songs(date)
print(hundred_songs)
list_of_uris=[]
for song in hundred_songs:
    result = sp.search(q=f'track:{song}', type='track', limit=1)
    tracks = result['tracks']['items']
    if tracks:
        uri = tracks[0]['uri']
        list_of_uris.append(uri)
    else:
        print(f"No results found for: {song}")

print(list_of_uris)
playlist=sp.user_playlist_create(user=user_id,name=f"{date} Billboard 100")
playlist_id=playlist['id']
sp.playlist_add_items(playlist_id=playlist_id, items=list_of_uris,position=0)