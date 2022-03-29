from flask import request
from flask import Blueprint
from flask import render_template, redirect, abort, flash
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse, urljoin
from werkzeug.security import generate_password_hash, check_password_hash

from service.auth.users import Users


def constructBlueprint(users: Users) -> Blueprint:
    airlineApi: Blueprint = Blueprint("airlineApi", __name__)
    aeAccount: dict = {
        "connected": False,
        "username": None,
        "password": None
    }

    @airlineApi.before_request
    def before_request():
        if not aeAccount["connected"]:
            return render_template(
                "auth/aeConnect.html",
            )

    # def renderLogin(
    #     postReqUrl: str = "/auth/login",
    #     username: str = "",
    #     errorMsg: str = None
    # ):
    #     return render_template(
    #         "auth/login.html",
    #         postReqUrl=postReqUrl,
    #         username=username,
    #         errorMsg=errorMsg
    #     )

    @airlineApi.route("/", methods=["GET"])
    # @airlineApi.route("/login", methods=["GET"])
    def airlinePage():
        return render_template(
            "airline.html",
        )

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

    # @airlineApi.route("/logout")
    # @login_required
    # def logout():
    #     users.setAuth(current_user.id, False)
    #     logout_user()
    #     flash("You were successfully logged out", "info")
    #     return redirect("/")

    return airlineApi