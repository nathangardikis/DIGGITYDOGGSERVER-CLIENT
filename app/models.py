from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import os

db = SQLAlchemy()
sourcepath = Path("C:/Users/Nathan/Desktop/MUSIC/")


class Users(db.Model):
    _id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=True)

    def __init__(self, _id, username, password, email):
        self._id = _id; self.username = username
        self.password = password; self.email = email

    def __repr__(self):
        return f"{self._id}-{self.username}"
    
class Requests(db.Model):
    _id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    catagory = db.Column(db.String(15), nullable=False)
    type = db.Column(db.String(15), nullable=False)
    content = db.Column(db.String(1500), nullable=False)
    user = db.Column(db.String(15), nullable=False)
    date = db.Column(db.String(15), nullable=False)
    img = db.Column(db.String(250), nullable=False)

    def __init__(self, _id, catagory, type, content, user, date, img):
        self._id = _id; self.catagory = catagory; self.type = type
        self.content = content; self.user = user; self.date = date
        self.img = img

    def __repr__(self):
        return f"{self._id}-{self.content}-{self.type}-{self.user}-{self.date}"

    

def list_current_requests():
    requests = []
    for request in os.listdir(sourcepath):
        requests.append(request)
    return requests

def to_str(num:int) -> str:
    return str(num)

def get_user_id():
    user_id = 0
    users = Users.query.all()
    for user in users:
        user_id += 1
    return user_id