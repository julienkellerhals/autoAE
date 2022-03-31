import pandas as pd
from flask import request
from flask import Blueprint
from flask import render_template, redirect

from ae.datastore import Datastore


def constructBlueprint(ds: Datastore) -> Blueprint:
    aircraftApi: Blueprint = Blueprint("aircraftApi", __name__, url_prefix="/aircraft")

    @aircraftApi.route("/", methods=["GET"])
    def aircraftPage():
        ds.getAircraftStats()
        aircraftStats: pd.DataFrame = ds.datastore["aircraftStats"]["aircraftStatsDf"]
        return render_template(
            "aircraft.html",
            aircraftStats=aircraftStats.to_html(index= False, escape=False),
        )

    return aircraftApi
