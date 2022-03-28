from flask import request
from flask import Blueprint
from flask import render_template, redirect, abort, flash
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse, urljoin
from werkzeug.security import generate_password_hash, check_password_hash


def constructBlueprint() -> Blueprint:
    authApi = Blueprint("loginApi", __name__)

    # def is_safe_url(target) -> bool:
        # ref_url = urlparse(request.host_url)
        # test_url = urlparse(urljoin(request.host_url, target))
        # return test_url.scheme in ('http', 'https') and \
        #     ref_url.netloc == test_url.netloc

    # def loginAction(username: str, password: str) -> bool:
    #     if username != "" and username is not None:
    #         userId: bytes = users.getMemberId(username)
    #         pwHash: str = users.getPasswordHash(username)
    #         if check_password_hash(pwHash, password):
    #             user = users.get(userId)
    #             if login_user(user):
    #                 users.setAuth(userId, True)
    #                 user.is_authenticated = True
    #                 return True
    #     return False

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

    # def renderRegister(
    #     postReqUrl: str = "/auth/register",
    #     sectionName: str = "",
    #     memberName: str = "",
    #     username: str = "",
    #     errorMsg: str = None
    # ):
    #     return render_template(
    #         "auth/register.html",
    #         postReqUrl=postReqUrl,
    #         sectionName=sectionName,
    #         memberName=memberName,
    #         username=username,
    #         errorMsg=errorMsg
    #     )

    # @authApi.route("/", methods=["GET"])
    # @authApi.route("/login", methods=["GET"])
    # def loginPage():
    #     return renderLogin(
    #         request.full_path
    #     )

    # @authApi.route("/register", methods=["GET"])
    # def registerPage():
    #     return renderRegister(
    #         request.full_path
    #     )

    # @authApi.route("/login", methods=["POST"])
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

    # @authApi.route("/register", methods=["POST"])
    # def register():
    #     sectionName = request.form.get("sectionName")
    #     memberName = request.form.get("memberName")
    #     username = request.form.get("username")
    #     password = request.form.get("password")
    #     pwHash = generate_password_hash(password)

    #     neoSection.createMember(
    #         sectionName,
    #         memberName,
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
    #             sectionName,
    #             memberName,
    #             username
    #         )

    # @authApi.route("/logout")
    # @login_required
    # def logout():
    #     users.setAuth(current_user.id, False)
    #     logout_user()
    #     flash("You were successfully logged out", "info")
    #     return redirect("/")

    return authApi