
from flask import request, redirect, url_for, render_template, session, Blueprint, flash
from werkzeug.utils import secure_filename
from .models import *
from .youtube_methods import *
from .permissions_methods import *
from .request_methods import *
from datetime import date

import hashlib, json

routes_bp = Blueprint("routes_bp", __name__, template_folder="templates")
coverpath = Path("C:/Users/Nathan/Desktop/Python Projects/ServerMusicAddHost/app/covers/")

# ROUTES
@routes_bp.route("/", methods=["POST", "GET"])
@routes_bp.route("/home", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        if "user" in session:
            user = str(session["user"])
            user_allowed = allow_user(user=user)
            requests = Requests.query.all()
            requests_in_progress = list_current_requests()
            admin_status = get_admin_status(username=user)
            general_settings = get_general_settings()
            user_settings = get_user(username=user)
            if user_allowed:
                return render_template("index.html", requests=reversed(requests), rip=requests_in_progress,
                                        user=user, admin_status=admin_status, general_settings=general_settings,
                                        user_settings=user_settings)
            else:
                return redirect(url_for("routes_bp.login"))
        else:
            return redirect(url_for("routes_bp.login"))
    elif request.method == "POST":
        query = request.form["query-form"]
        _type = request.form["type-form"]
        if _type == "Artist":
            return redirect(url_for("dz_results.deezer_artist_results", query=query))
        elif _type == "Album":
            return redirect(url_for("dz_results.deezer_album_results", query=query))
        elif _type == "URL":
            pass
            

@routes_bp.route("/url-request", methods=["POST", "GET"])
@routes_bp.route("/url-request/", methods=["POST", "GET"])
def url_request():
    if request.method == "GET":
        if "user" in session:
            user = str(session["user"])
            user_allowed = allow_user(user=user)
            if user_allowed:
                return render_template("url_request.html", user=user)
            else:
                return redirect(url_for("routes_bp.login"))
    elif request.method == "POST":
        if "user" in session:
            user = str(session["user"])
            user_exists = Users.query.filter_by(username=user).first()
            requests = Requests.query.all()
            requests_in_progress = list_current_requests()
            request_id = get_request_id()

            url_type = request.form["api-form"]
            url = request.form["url-form"]
            audio_format = request.form[f"{url_type}-format-form"]

            if url_type == "Youtube":

                cover_photo_file = request.files["cover-photo-form"]
                cover_photo_filename = secure_filename(cover_photo_file.filename)
                new_coverpath = os.path.join(coverpath, str(request_id))
                create_request_dir(path=new_coverpath)
                cover_photo_file.save(os.path.join(new_coverpath, cover_photo_filename))

                artist_name = request.form["artist-name-form"]
                request_title = request.form["request-title-form"]
                
                data = {
                    "catagory": "Music",
                    "type": "Url",
                    "api": url_type,
                    "content": request_title,
                    "artist": artist_name,
                    "date": str(date.today()),
                    "bitrate": get_audio_format(audio_format),
                    "user": session["user"],
                    "id": request_id,
                    "img": os.path.join(new_coverpath, cover_photo_filename),
                    "url": url
                }

                initialize_request(data=data)

            if user_exists:
                return redirect(url_for("routes_bp.index", requests=reversed(requests), rip=requests_in_progress, user=user))
            else:
                return redirect(url_for("routes_bp.login"))


@routes_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if "user" in session:
            session.pop("user")
        return render_template("login.html", general_settings=get_general_settings())
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()    
        found_user = Users.query.filter_by(username=username).first()
        if found_user:
            if str(hashed_password) == str(found_user.password):
                session["user"] = username
                return redirect(url_for("routes_bp.index"))
        else:
            flash("Erorror loggin in", "error")
            return redirect(url_for("routes_bp.login"))
        


@routes_bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        if "user" in session:
            session.pop("user")
        return render_template("register.html")
    elif request.method == "POST":
        permissions = get_permissions()
        newusername = request.form["newusername"]
        newpassword = request.form["newpassword"]
        newemail = request.form["newemail"]
        hashed_password = hashlib.sha256(newpassword.encode()).hexdigest()
        existing_user = Users.query.filter_by(username=newusername).first()
        if existing_user:
            return redirect(url_for("routes_bp.register"))
        else:
            new_user = Users(_id=get_user_id(), username=newusername, password=hashed_password, email=newemail)
            add_user(user=newusername, email=newemail)
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)
            return redirect(url_for("routes_bp.login"))
        
@routes_bp.route("/verify/<email>", methods=["GET"])
def verify(email):
    if request.method == "GET":
        permissions = get_permissions()
        p_emails = permissions["emails"]
        for pe in p_emails:
            if str(pe["email"].lower()) == str(email.lower()):
                if pe["registered"] == True:
                    return "active"
                elif pe["registered"] == False:
                    return "found"
        return "missing"
    return "python error"

@routes_bp.route("/admin", methods=["POST", "GET"])
def admin():
    if request.method == "GET":
        if "user" in session:
            permissions = get_permissions()
            user = str(session["user"])
            db_users = Users.query.all()
            p_file = json.dumps(permissions)
            for p_user in permissions["users"]:
                if p_user["username"] == user:
                    if p_user["admin"] == True:
                        return render_template("admin.html", user=user, db_users=db_users, permissions=permissions, p_file=p_file)
            return redirect(url_for("routes_bp.index"))
        else:
            return redirect(url_for("routes_bp.index"))
        
@routes_bp.route("/apply-general", methods=["POST", "GET"])
def apply_general_settings():
    if request.method == "GET":
        return 404
    elif request.method == "POST":
        new_general_settings = request.json
        update_general(general=new_general_settings)
        return "general updated"
    
@routes_bp.route("/apply-user", methods=["POST", "GET"])
def apply_user_settings():
    if request.method == "GET":
        return get_users()
    elif request.method == "POST":
        new_user_settings = request.json
        update_users(users=new_user_settings)
        return "user updated"
    
@routes_bp.route("/get-user-from-email/<email>", methods=["POST", "GET"])
def get_user_route(email):
    if request.method == "GET":
        username = get_username_from_email(email=email)
        return username