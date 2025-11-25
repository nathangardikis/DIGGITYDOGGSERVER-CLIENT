from flask import request, redirect, url_for, render_template, session, Blueprint
from app.models import *
from app.spotify_methods import *
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#SPOTIFY CLIENT
secret = "c1c057bd2b824447926987ba8d0336b0"
id = "58bd345aeacd43188b3c3532c1b8a617"
ccm = SpotifyClientCredentials(client_id=id, client_secret=secret)
client = spotipy.Spotify(client_credentials_manager=ccm)

sp_results = Blueprint("sp_results", __name__, template_folder="results_templates")


@sp_results.route("/spotify/artist/results/<query>", methods=["POST", "GET"])
def spotify_artist_results(query):
    discography = get_spotify_discography(artist_name=query)
    user_exists = Users.query.filter_by(username=session["user"]).first()
    if "user" in session:
        if user_exists:
            if request.method == "GET":
                return render_template("results.html", discography=discography)
