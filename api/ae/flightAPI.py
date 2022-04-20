import pandas as pd
from flask import Blueprint, request, redirect
from flask import render_template

from ae.datastore import Datastore


def constructBlueprint(ds: Datastore) -> Blueprint:
    flightApi: Blueprint = Blueprint("flightApi", __name__, url_prefix="/flight")

    @flightApi.route("/", methods=["GET"])
    def flightPage():
        flightList: pd.DataFrame = ds.datastore["flightsList"]["flightsListDf"]
        return render_template(
            "flight.html",
            flightList=flightList.to_html(index= False, escape=False),
        )

    @flightApi.route("/use", methods=["GET"])
    def flightSearchPage():
        df = ds.datastore["aircraftStats"]["aircraftStatsDf"]
        aircraft = df[df["aircraft"].str.contains(request.args["aircraft"], regex=False)]
        return render_template(
            "flight.html",
            postReqUrl = "/ae/flight/use?aircraft=" + request.args["aircraft"],
            range = aircraft["range"].values[0]

        )

    @flightApi.route("/use", methods=["POST"])
    def flightSearch():
        df = ds.datastore["aircraftStats"]["aircraftStatsDf"]
        aircraft = df[df["aircraft"].str.contains(request.args["aircraft"], regex=False)]
        runway = aircraft["minRunway"].values[0]
        ds.datastore["flightsList"]["searchParams"]["country"] = request.values["country"]
        ds.datastore["flightsList"]["searchParams"]["region"] = request.values["region"]
        ds.datastore["flightsList"]["searchParams"]["runway"] = runway
        ds.datastore["flightsList"]["searchParams"]["rangemin"] = request.values["rangemin"]
        ds.datastore["flightsList"]["searchParams"]["rangemax"] = request.values["rangemax"]
        ds.datastore["flightsList"]["searchParams"]["city"] = request.values["city"]
        ds.getFlights()
        # flightList: pd.DataFrame = ds.datastore["flightsList"]["flightsListDf"]
        return redirect("/ae/flight")

    return flightApi
