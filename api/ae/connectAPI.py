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
    connectApi: Blueprint = Blueprint("connectApi", __name__, url_prefix="/connect")

    @connectApi.route("/", methods=["GET"])
    def connectPage():
        return render_template(
            "auth/aeConnect.html",
        )


    @connectApi.route("/", methods=["POST"])
    def connect():
        username = request.form.get("username")
        password = request.form.get("password")
        ds.login(username, password)

        return redirect("/ae/airlines")

    return connectApi
