from flask import request
from flask import Blueprint
from flask import render_template, redirect

from ae.datastore import Datastore


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
