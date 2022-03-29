from flask import Flask
from flask import render_template
from flask_login import LoginManager

from api import authAPI
from api import airlineAPI
from service.auth.users import Users


app = Flask(__name__)
app.secret_key = (
    "192b9bdd22ab9ed4d12e236c78afcb"
    "9a393ec15f71bbf5dc987d54727823bcbf"
)

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "/auth/login"
users = Users()


@loginManager.user_loader
def load_user(userId):
    return users.get(userId)


@app.route('/')
def base():
    return render_template(
        "base.html"
    )


app.register_blueprint(authAPI.constructBlueprint(
        users
    ),
    url_prefix="/auth"
)


app.register_blueprint(airlineAPI.constructBlueprint(
        users
    ),
    url_prefix="/airline"
)


if __name__ == '__main__':
    app.run(debug=True)