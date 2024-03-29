from flask import Blueprint
from flask import render_template

from api.ae import flightAPI
from api.ae import connectAPI
from api.ae import airlinesAPI
from api.ae import aircraftAPI
from ae.datastore import Datastore


def constructBlueprint() -> Blueprint:
    aeApi: Blueprint = Blueprint("aeApi", __name__)
    ds: Datastore = Datastore()

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

    aeApi.register_blueprint(aircraftAPI.constructBlueprint(
            ds
        ),
        url_prefix="/aircraft"
    )

    aeApi.register_blueprint(flightAPI.constructBlueprint(
            ds
        ),
        url_prefix="/flight"
    )

    return aeApi
