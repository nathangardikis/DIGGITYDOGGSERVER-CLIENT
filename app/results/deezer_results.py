from flask import request, redirect, url_for, session, render_template, Blueprint
from app.models import *
from datetime import date
from app.deezer_methods import *
from app.request_methods import *

dz_results = Blueprint("dz_results", __name__, template_folder="results_templates")


@dz_results.route("/artist/<query>", methods=["POST", "GET"])
def deezer_artist_results(query):
    user_exists = get_user_status()
    if user_exists:
        if request.method == "GET":
            artists = get_deezer_artists(query)
            return render_template("deezer_artist_results.html", query=query, artists=artists)
        elif request.method == "POST":
            data = {
                "catagory": "Music",
                "type": "Artist",
                "content": request.form["artist_name"],
                "artist": request.form["artist_name"],
                "date": str(date.today()),
                "bitrate": get_bitrate(request.form["bitrate"]),
                "user": session["user"],
                "id": get_request_id(),
                "img": request.form["img_source"]
            }
            initialize_request(data=data)
            return redirect(url_for("routes_bp.index"))
    else:
        return redirect(url_for("routes_bp.login"))

@dz_results.route("/album/<query>", methods=["POST", "GET"])
def deezer_album_results(query):
    user_exists = Users.query.filter_by(username=session["user"]).first()
    if request.method == "GET":
        if "user" in session:
            if user_exists:
                albums = get_deezer_albums(query)
                return render_template("deezer_album_results.html", query=query, albums=albums)
    elif request.method == "POST":
        if "user" in session:
            if user_exists:
                data = {
                    "catagory": "Music",
                    "type": "Album",
                    "content": request.form["artist_name"] + " - " + request.form["album_name"],
                    "artist": request.form["artist_name"],
                    "title": request.form["album_name"],
                    "date": str(date.today()),
                    "bitrate": get_bitrate(request.form["bitrate"]),
                    "user": session["user"],
                    "id": get_request_id(),
                    "img": request.form["img_source"]
                }
                initialize_request(data=data)
                return redirect(url_for("routes_bp.index"))