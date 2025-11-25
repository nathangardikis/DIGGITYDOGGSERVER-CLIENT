import secrets


class Config:
    SECRET_KEY = secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "C:/Users/Nathan/Desktop/Python Projects/ServerMusicAddHost/app/uploads"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}