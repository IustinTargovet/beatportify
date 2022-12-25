import spotipy

from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

from Track import Track

from datetime import datetime


# Get the current date and time

def get_date_string():
    now = datetime.now()
    # Format the date as dd-mm-yy using the strftime method
    date_str = now.strftime("%d-%m-%y")
    return date_str


# Replace this with the URL of the webpage you want to scrape
# Afro-House: https://www.beatport.com/genre/afro-house/89/top-100
# Tech-House: https://www.beatport.com/genre/tech-house/11/top-100
# Funky-House: https://www.beatport.com/genre/funky-house/81/top-100
# Top-100: https://www.beatport.com/top-100
url = "https://www.beatport.com/genre/tech-house/11/top-100"
tracks_to_add = []

# Send an HTTP request to the URL
response = requests.get(url)

# Parse the HTML response
soup = BeautifulSoup(response.text, "html.parser")

# Find all elements with the specified class
elements = soup.select(".buk-track-meta-parent")

# Print the elements
index = 0

for element in elements:
    tracks_to_add.append(Track.from_buk_track_meta_parent_element(element))

scope = ["playlist-modify-private", "playlist-modify-public", "user-library-read"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id='<your_client_id>',
                                               client_secret='<your_client_secret>',
                                               redirect_uri='http://localhost:6060'))

# going through track list and adding to new playlist
tracks_to_add_uris = []

for track in tracks_to_add:
    results = sp.search(q=f"track:{track.title} artist:{track.artist}", type="track")
    if len(results["tracks"]["items"]) > 0:
        print(f"{track.title} - {track.artist} found")
        song = results["tracks"]["items"][0]
        tracks_to_add_uris.append(song["uri"])
    else:
        print(f"{track.title} - {track.artist} NOT found")
        results = sp.search(q=f"track:{track.title}", type="track")
        if len(results["tracks"]["items"]) > 0:
            print(f"{track.title} found")
            song = results["tracks"]["items"][0]
            tracks_to_add_uris.append(song["uri"])
        else:
            print(f"{track.title} NOT found")


# create playlist and add all found uris

def create_name_from_beatport_url(url):
    index_of_genre = -1
    if "genre" in url:
        index_of_genre = -3
    return url.split("/")[index_of_genre] + " " + get_date_string()


playlist_name = create_name_from_beatport_url(url)


def create_description_from_beatport_url(url):
    return "Playlist computationally created with love to follow the " + url.split("/")[-1] + " on beatport at " + get_date_string()


playlist_description = create_description_from_beatport_url(url)

print("Creating playlist")
playlist = sp.user_playlist_create(
    sp.me()["id"], playlist_name, public=True, description=playlist_description
)
print("Playlist created successfully")

# Get the playlist ID
playlist_id = playlist["id"]

# Add the songs to the playlist
print("Add songs by URI")
sp.playlist_add_items(playlist_id, tracks_to_add_uris)
print(f"Added {len(tracks_to_add_uris)} tracks successfully")

