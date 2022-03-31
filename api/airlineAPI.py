from urllib.parse import urlparse, urljoin
import pandas as pd
from flask import request
from flask import Blueprint
from flask import render_template, redirect, abort, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from ae.datastore import Datastore
from service.auth.users import Users


def constructBlueprint(users: Users) -> Blueprint:
    airlineApi: Blueprint = Blueprint("airlineApi", __name__)
    ds: Datastore = Datastore()

    @airlineApi.before_request
    def before_request():
        if request.method == "GET":
            if ("status" not in ds.datastore["login"].keys()
                or not ds.datastore["login"]["status"]):
                return render_template(
                    "auth/aeConnect.html",
                )

# TODO create data store with eg all available airlines
# and create a kind of validity where data only get stored for x min
# TODO use stream to pipe first 5 error messages

    @airlineApi.route("/", methods=["GET"])
    def airlinePage():
        ds.getWorld()
        airlineDf: pd.DataFrame = ds.datastore["airlines"]["airlineDf"]
        return render_template(
            "airline.html",
            airlines=airlineDf.to_html(escape=False),
        )

    @airlineApi.route("/world", methods=["GET"])
    def worldPage():
        ds.enterWorld(request.args.get("world"), request.args.get("player"))
        return redirect("/")

    # @airlineApi.route("/login", methods=["POST"])
    # def login():
    #     username = request.form.get("username")
    #     password = request.form.get("password")
    #     if loginAction(username, password):
    #         next = request.args.get("next")
    #         if is_safe_url(next):
    #             flash("You were successfully logged in", "info")
    #             return redirect(next or "/")
    #         else:
    #             return abort(400)
    #     else:
    #         return renderLogin(
    #             request.full_path,
    #             username,
    #             "Login Failed"
    #         )

    # @airlineApi.route("/register", methods=["POST"])
    # def register():
    #     username = request.form.get("username")
    #     password = request.form.get("password")
    #     pwHash = generate_password_hash(password)

    #     users.createUser(
    #         username,
    #         pwHash
    #     )
    #     if loginAction(username, password):
    #         next = request.args.get("next")
    #         if is_safe_url(next):
    #             flash("You were successfully logged in", "info")
    #             return redirect(next or "/")
    #         else:
    #             return abort(400)
    #     else:
    #         return renderRegister(
    #             request.full_path,
    #             username
    #         )

    @airlineApi.route("/aeConnect", methods=["POST"])
    def aeConnect():
        username = request.form.get("username")
        password = request.form.get("password")
        ds.login(username, password)

        return redirect("/airline/")

    return airlineApi
