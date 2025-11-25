import spotipy, os
from pathlib import Path
from threading import Thread
from spotipy.oauth2 import SpotifyClientCredentials


root_path = os.path.normpath(os.getcwd())


# CREATE SPOTIFY CLIENT
secret = "c1c057bd2b824447926987ba8d0336b0"
id = "58bd345aeacd43188b3c3532c1b8a617"
ccm = SpotifyClientCredentials(client_id=id, client_secret=secret)
client = spotipy.Spotify(client_credentials_manager=ccm)


# METHODS
def get_artist_id(artist_name:str) -> str:
    results = client.search(q=artist_name, type="artist")
    artist = results["artists"]["items"][0]
    return artist["id"]

def get_artist(artist_name:str) -> dict:
    results = client.search(q=artist_name, type="artist")
    artist = results["artists"]["items"][0]
    return artist
    
def get_artist_url(artist:dict) -> str:
    url = artist["external_urls"][0]["spotify"]
    return url

def get_album_url(album:dict) -> str:
    url = album["external_urls"][0]["spotify"]
    return url
    
def get_artists(query:str) -> dict:
    results = client.search(q=query, type="artist")
    artists = results["artists"]["items"]
    return artists


def get_artist_albums(artist_id:str) -> list:
    album_list = []
    results = client.artist_albums(artist_id, album_type="album")
    albums = results["items"]
    while results["next"]:
        results = client.next(results)
        albums.extend(results["items"])
    for album in albums:
        album_list.append(album)
    return album_list


def get_artist_album(artist_name:str, album_title:str) -> dict:
    artist_albums = get_artist_albums(artist_id=get_artist_id(artist_name=artist_name))
    artist_album = None
    for album in artist_albums:
        if album_title.lower() == album["name"].lower():
            artist_album = album
    return artist_album


def get_artist_eps(artist_id:str) -> list:
    ep_list = []
    results = client.artist_albums(artist_id, album_type="single")
    eps = results["items"]
    while results["next"]:
        results = client.next(results)
        eps.extend(results["items"])
    for ep in eps:
        ep_list.append(ep)
    return ep_list

def get_album_tracks(album_uri:str) -> list:
    _album_tracks = []
    results = client.album_tracks(album_uri)
    album_tracks = results["items"]
    while results["next"]:
        results = client.next(results)
        album_tracks.extend(results["items"])
    for track in album_tracks:
        _album_tracks.append(track["name"])
    return _album_tracks

def get_top_tracks(artist_id:str) -> list:
    top_tracks = client.artist_top_tracks(artist_id)
    _top_tracks = []
    tracks = top_tracks["tracks"]
    for t in range(len(tracks)):
        track = tracks[t]
        _track = {
            "title": track["name"],
            "cover": track["album"]["images"][0]["url"],
            "#": int(t + 1)
        }
        _top_tracks.append(_track)
    return _top_tracks

def get_spotify_discography(artist_name:str) -> dict:
    artist = get_artist(artist_name=artist_name)
    albums = get_artist_albums(artist_id=artist["id"])
    eps = get_artist_eps(artist_id=artist["id"])
    top_tracks = get_top_tracks(artist_id=artist["id"])
    _albums = []
    _eps = []
    for album in albums:
        _tracks = []
        tracks = get_album_tracks(album["uri"])
        for track in range(len(tracks)):
            t = {
                "title": tracks[track],
                "artist": artist["name"],
                "#": int(track + 1)
            }
            _tracks.append(t)
        _album = {
            "title": album["name"],
            "cover": album["images"][0]["url"],
            "tracks": _tracks
        }
        _albums.append(_album)
    for ep in eps:
        _tracks = []
        tracks = get_album_tracks(ep["uri"])
        for track in range(len(tracks)):
            t = {
                "title": tracks[track],
                "artist": artist["name"],
                "#": int(track + 1)
            }
            _tracks.append(t)
        _ep = {
            "title": ep["name"],
            "cover": ep["images"][0]["url"],
            "tracks": _tracks
        }
        _eps.append(_ep)
    discography = {
        "name": artist["name"],
        "request-type": "artist",
        "artist_img": artist["images"][0]["url"],
        "albums": _albums,
        "eps": _eps,
        "top_tracks": top_tracks,
        "artist_name": artist_name
    }
    return discography
    
def run_spotdl(url:str, dest_path) -> None:
    os.chdir(dest_path)
    os.system(f"spotdl {url}")
    os.chdir(root_path)