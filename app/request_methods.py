from .models import *
from .deezer_methods import *
from .spotify_methods import *
from .youtube_methods import *
from threading import Thread
from flask import session
import shutil


sourcepath = Path("C:/Users/Nathan/Desktop/MUSIC/")
coverpath = Path("C:/Users/Nathan/Desktop/Python Projects/ServerMusicAddHost/app/covers/")


def get_user_status() -> bool:
    if "user" in session:
        user = Users.query.filter_by(username=session["user"]).first()
        if user:
            return True
        else:
            return False
    else:
        return False


def get_request_id() -> int:
    request_id = len(Requests.query.all())
    return request_id


def artist_exists(artist:str):
    exists = False
    for dir in os.listdir(destpath):
        if dir.lower() == artist.lower():
            exists = True
    return exists


def create_artist_dir(artist:str):
    os.mkdir(os.path.join(destpath, artist))


def create_request_dir(path:Path):
    os.mkdir(path)


def move_requested_files(source_path:str, dest_path:str, request_id:str):
    request_path = None
    for dir in os.listdir(source_path):
        if dir.lower() == str(request_id).lower():
            request_path = os.path.join(source_path, dir)
    print("Request path created...")
    for dir in os.listdir(request_path):
        content = os.path.join(request_path, dir)
        try:
            shutil.move(content, dest_path)
        except shutil.Error:
            print(f"[ERROR]: {shutil.Error}")
        print(f"[ {dir} ] successfully moved to [ {dest_path} ]...")
    os.rmdir(request_path)



def get_bitrate(bitrate:str) -> str:
    if bitrate == "MP3_128":
        return "128"
    elif bitrate == "MP3_254":
        return "254"
    elif bitrate == "MP3_320":
        return "320"
    elif bitrate == "FLAC":
        return "flac"
    else:
        return "320"
    

def get_audio_format(audio_format:str) -> str:
    if audio_format == "MP3 128 Kbps":
        return "128"
    elif audio_format == "MP3 256 Kbps":
        return "256"
    elif audio_format == "MP3 320 Kbps ⭐":
        return "320"
    elif audio_format == "FLAC 44.1/16 ⭐":
        return "flac"
    else:
        return "320"


def add_request_to_db(data:dict) -> None:
    new_request = Requests (
        _id=data["id"],
        catagory=data["catagory"],
        type=data["type"],
        content=data["content"],
        user=data["user"],
        date=data["date"],
        img=data["img"]
    )
    db.session.add(new_request)
    db.session.commit()
    db.session.refresh(new_request)


def complete_request(request_id:str, artist_name:str):
    if artist_exists(artist=artist_name) == True:
        pass
    else:
        create_artist_dir(artist=artist_name)
    artist_path = os.path.join(destpath, artist_name)
    move_requested_files(source_path=sourcepath, dest_path=artist_path, request_id=request_id)
    print(f"REQUEST [{request_id}] COMPLETE...")


def submit_artist_request(data:dict) -> None:
    deezer_artist_url = get_deezer_artist_url(artist_name=data["content"])
    if deezer_artist_url is not None:
        new_path = "C:/Users/Nathan/Desktop/MUSIC/" + str(data["id"])
        create_request_dir(new_path)
        run_deemix(url=deezer_artist_url, bitrate=data["bitrate"], path=new_path)
        complete_request(request_id=data["id"], artist_name=data["artist"])
    else:
        new_path = "C:/Users/Nathan/Desktop/MUSIC/" + str(data["id"])
        spotify_artist = get_artist(artist_name=data["content"])
        spotify_artist_url = get_artist_url(artist=spotify_artist)
        run_spotdl(url=spotify_artist_url, dest_path=new_path)


def submit_album_request(data:dict) -> None:
    deezer_album_url = get_deezer_album_url(album_title=data["title"], artist=data["artist"])
    if deezer_album_url is not None:
        new_path = "C:/Users/Nathan/Desktop/MUSIC/" + str(data["id"])
        create_request_dir(new_path)
        run_deemix(url=deezer_album_url, bitrate=data["bitrate"], path=new_path)
        complete_request(request_id=data["id"], artist_name=data["artist"])
    else:
        spotify_album = get_artist_album(artist_name=data["artist"], album_title=data["title"])
        spotify_album_url = get_album_url(album=spotify_album)
        run_spotdl(url=spotify_album_url)

def submit_url_request(data:dict) -> None:
    url = data["url"]
    if url is not None:
        new_path = "C:/Users/Nathan/Desktop/MUSIC/" + str(data["id"])
        create_request_dir(new_path)
        if data["api"] == "Youtube":
            start_ytdlp(path=new_path, url=data["url"], bitrate=data["bitrate"])
            mp3_file_name = get_old_mp3_filename(path=new_path)
            new_mp3_file_name = get_new_mp3_filename(artist=data["artist"], title=data["content"])
            new_mp3_file_path = f"{new_path}/{new_mp3_file_name}"
            metadata = {
                "artist": data["artist"],
                "title": data["content"],
                "album": data["content"],
                "id": data["id"],
                "img": data["img"]
            }
            change_mp3_file_name(path=new_path, old_filename=mp3_file_name, new_filename=new_mp3_file_name)
            change_mp3_file_metadata(filepath=new_mp3_file_path, metadata=metadata)
            complete_request(request_id=data["id"], artist_name=data["artist"])


def initialize_request(data:dict) -> None:
    add_request_to_db(data=data)
    if data["type"] == "Artist":
        Thread(target=submit_artist_request, args=(data,)).start()
    elif data["type"] == "Album":
        Thread(target=submit_album_request, args=(data,)).start()
    elif data["type"] == "Url":
        Thread(target=submit_url_request, args=(data,)).start()

