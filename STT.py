import os
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"), #this is your Spotify developer app client ID
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"), #this is your Spotify developer app client secret
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"), #this is your Spotify developer app redirect URL you set this is important because when you run script at the end it will ask for playlist URL and then it will ask the URL it redirects after authorisation
    scope="playlist-read-private"
))

# Function to sanitize filenames
def sanitize_filename(name):
    # Replace invalid characters with underscores
    return re.sub(r'[\\/*?:"<>|]', "_", name)

# Function to get playlist details
def get_playlist_details(playlist_id):
    playlist = sp.playlist(playlist_id)
    return playlist['name'], playlist['tracks']

# Function to save playlist to a text file
def save_playlist_STT(playlist_id):
    playlist_name, tracks = get_playlist_details(playlist_id)
    filename = f"{sanitize_filename(playlist_name)}.txt"  # Use sanitized playlist name as the filename
    with open(filename, "w", encoding="utf-8") as file:
        for item in tracks['items']:
            track = item['track']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            file.write(f"{track_name} - {artist_name}\n")
    print(f"Playlist '{playlist_name}' saved to {filename}")

# Main script
if __name__ == "__main__":
    playlist_link = input("Enter the Spotify playlist link: ")
    playlist_id = playlist_link.split("/")[-1].split("?")[0]  # Extract playlist ID from link
    save_playlist_STT(playlist_id)