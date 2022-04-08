from flask import Blueprint
from flask import render_template

from ae.datastore import Datastore


def constructBlueprint(ds: Datastore) -> Blueprint:
    flightApi: Blueprint = Blueprint("flightApi", __name__, url_prefix="/flight")

    @flightApi.route("/", methods=["GET"])
    def flightPage():
        return render_template(
            "flight.html",
        )

    # TODO implement use

    return flightApi
