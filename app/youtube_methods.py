import os
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC


root_path = os.path.normpath(os.getcwd())


def get_mp3_command(url:str, path:str, bitrate) -> str:
    return f'yt-dlp -x --audio-quality "{bitrate}" --audio-format "mp3" --ffmpeg-location "C:/Program Files/ffmpeg/bin" -P "{path}" "{url}"'


def start_ytdlp(path:str, url:str, bitrate) -> None:
    ytdlp_command = get_mp3_command(url=url, path=path, bitrate=bitrate)
    os.system(ytdlp_command)
    print("ytdlp finished")

def get_old_mp3_filename(path) -> str:
    files = os.listdir(path)
    if len(files) == 1:
        for file in files:
            return file

def get_new_mp3_filename(artist:str, title:str) -> str:
    return f"{artist} - {title}.mp3"

def change_mp3_file_name(path, old_filename, new_filename):
    cwd = os.getcwd()
    os.chdir(path)
    try:
        os.rename(old_filename, new_filename)
    except FileNotFoundError:
        print(f"[ ERROR ]: {old_filename} not found...")
    except:
        print("[ ERROR ]: Unkown error")
    os.chdir(cwd)

def change_mp3_file_metadata(filepath, metadata) -> None:
    with open(metadata["img"], "rb") as coverfile:
        cover_image = coverfile.read()
    mp3_file = MP3(filepath, ID3=ID3)
    mp3_file["TIT2"] = TIT2(encoding=3, text=[metadata["title"]])
    mp3_file["TALB"] = TALB(encoding=3, text=[metadata["album"]])
    mp3_file["TPE1"] = TPE1(encoding=3, text=[metadata["artist"]])
    mp3_file["APIC"] = APIC(encoding=0, mime="image/jpeg", type=3,
                            desc=u"Cover", data=cover_image)
    mp3_file.save()
