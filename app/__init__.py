from flask import Flask, request, redirect, url_for, render_template
from pathlib import Path
from app.config import Config
from app.models import db
from app.routes import routes_bp
from .results.deezer_results import dz_results
from .results.spotify_results import sp_results
import os


root_path = os.path.normpath(os.getcwd())
destpath = Path("//DESKTOP-FK8LUSQ/music")

def create_app() -> Flask:

    a = Flask(__name__)
    
    a.config.from_object(Config)
    
    try:
        os.makedirs(a.instance_path) 
    except OSError:
        pass

    db.init_app(a)
    with a.app_context():
        db.create_all()

    import app.models

    
    a.register_blueprint(routes_bp, url_prefix="/auth")
    a.register_blueprint(dz_results, url_prefix="/deezer")
    a.register_blueprint(sp_results, url_prefix="/spotify")

    @a.route("/", methods=["Get"])
    @a.route("/home", methods=["GET"])
    def home():
        if request.method == "GET":
            return redirect(url_for("routes_bp.index"))
        else:
            return render_template("/static/404.html")

    return a

