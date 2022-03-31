from urllib.parse import urlparse, urljoin
import pandas as pd
from flask import request
from flask import Blueprint
from flask import render_template, redirect, abort, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from ae.datastore import Datastore
from service.auth.users import Users


def constructBlueprint(ds: Datastore) -> Blueprint:
    airlinesApi: Blueprint = Blueprint("airlinesApi", __name__, url_prefix="/airlines")

    @airlinesApi.route("/", methods=["GET"])
    def airlinesPage():
        ds.getWorld()
        airlineDf: pd.DataFrame = ds.datastore["airlines"]["airlineDf"]
        return render_template(
            "airlines.html",
            airlines=airlineDf.to_html(escape=False),
        )

    @airlinesApi.route("/join", methods=["GET"])
    def airlinesJoin():
        ds.enterWorld(request.args.get("world"), request.args.get("player"))
        return redirect("/ae/")

    return airlinesApi
