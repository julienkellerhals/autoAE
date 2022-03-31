from urllib.parse import urlparse, urljoin
import pandas as pd
from flask import request
from flask import Blueprint
from flask import render_template, redirect, abort, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from api.ae import connectAPI
from api.ae import airlinesAPI
from ae.datastore import Datastore


def constructBlueprint() -> Blueprint:
    aeApi: Blueprint = Blueprint("aeApi", __name__)
    ds: Datastore = Datastore()

    # @aeApi.before_request
    # def before_request():
    #     if request.method == "GET":
    #         if ("status" not in ds.datastore["login"].keys()
    #             or not ds.datastore["login"]["status"]):
    #             return redirect("/ae/connect")

    @aeApi.route("/", methods=["GET"])
    def aePage():
        return render_template(
            "base.html",
        )

    aeApi.register_blueprint(connectAPI.constructBlueprint(
            ds
        ),
        url_prefix="/connect"
    )

    aeApi.register_blueprint(airlinesAPI.constructBlueprint(
            ds
        ),
        url_prefix="/airlines"
    )

    return aeApi
