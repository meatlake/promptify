import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from ai import extract_keywords
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-modify-public"
))

async def create_playlist_from_prompt(prompt):
    keywords = extract_keywords(prompt)
    tracks = []
    for word in keywords:
        results = sp.search(q=word, limit=5, type='track')
        tracks += [item['id'] for item in results['tracks']['items']]
    
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user_id, name=f"AI Playlist: {prompt}", public=True)
    sp.playlist_add_items(playlist_id=playlist["id"], items=tracks[:30])
    return playlist["external_urls"]["spotify"]
