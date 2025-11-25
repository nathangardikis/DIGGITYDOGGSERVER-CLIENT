import os, deezer_python
from pathlib import Path


root_path = os.path.normpath(os.getcwd())
destpath = Path("//DESKTOP-FK8LUSQ/music")

# CREATE DEEZER CLIENT
dz = deezer_python.Client()

# METHODS 
def get_deezer_results(query:str) -> list:
    results = dz.search(query)
    return results

def get_deezer_track_url(title: str, artist: str) -> str:
    track_title = f"{artist} {title}"
    results = dz.search(track_title)
    for track in results:
        if track.artist.name.lower() == artist.lower():
            return track.link
    
def get_deezer_albums(album_title: str):
    
    results = dz.search_albums(album_title)
    return results

def get_deezer_album_url(album_title: str, artist: str) -> str:
    results = dz.search_albums(album_title)
    for album in results:
        if album.title.lower() == album_title.lower() and album.artist.name.lower() == artist.lower():
            return album.link
            
def get_deezer_artist(artist_name: str):
    results = dz.search_artists(artist_name)
    output = None
    for result in results:
        if result.name.lower() == artist_name.lower():
            output = result
    return output
            
def get_deezer_artists(artist_name: str) -> list:
    artists = []
    results = dz.search_artists(artist_name)
    for artist in results:
        a = {
            "name": artist.name,
            "img": artist.picture,
            "url": artist.link
        }
        artists.append(a)
    return artists

def get_deezer_artist_url(artist_name: str) -> str:
    results = dz.search_artists(artist_name)
    for result in results:
        if result.name.lower() == artist_name.lower():
            return result.link
        else:
            return None

def run_deemix(url:str, bitrate:str, path:Path) -> None:
    command = f"deemix {url} -b {bitrate} -p {path}"
    os.system(command)