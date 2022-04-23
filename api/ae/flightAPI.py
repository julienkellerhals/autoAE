from threading import Thread
import pandas as pd
from flask import Blueprint, request, redirect
from flask import render_template

from ae.datastore import Datastore


def constructBlueprint(ds: Datastore) -> Blueprint:
    flightApi: Blueprint = Blueprint("flightApi", __name__, url_prefix="/flight")

    @flightApi.route("/", methods=["GET"])
    def flightPage():
        flightList: pd.DataFrame = ds.datastore["flightsList"]["flightsListDf"]
        if "aircraft" in request.args:
            postReqUrl = "/ae/flight/create?aircraft=" + request.args["aircraft"]
        else:
            postReqUrl = "/ae/flight/create"
        return render_template(
            "flight.html",
            postReqUrl = postReqUrl,
            flightList=flightList.to_html(index= False, escape=False),
        )

    @flightApi.route("/create", methods=["POST"])
    def flightCreate():
        flightParams = {}
        paramList = [
            "reducedCap",
            "autoSlots",
            "autoTerminal",
            "autoHub"
        ]
        for param in paramList:
            if request.values[param] == "1":
                flightParams[param] = True
            else:
                flightParams[param] = False
        flightParams["minFreq"] = request.values["minFreq"]
        flightParams["maxFreq"] = request.values["maxFreq"]

        ds.datastore["flightsList"]["flightParams"] = flightParams

        thread = Thread(
            target=ds.createFlights,
            args=(request.args["aircraft"],)
        )
        thread.daemon = True
        thread.start()
        return redirect("/ae/flight")

    @flightApi.route("/use", methods=["GET"])
    def flightSearchPage():
        df = ds.datastore["aircraftStats"]["aircraftStatsDf"]
        aircraft = df[df["aircraft"].str.contains(request.args["aircraft"], regex=False)]
        return render_template(
            "flight.html",
            mode="use",
            postReqUrl = "/ae/flight/use?aircraft=" + request.args["aircraft"],
            range = aircraft["range"].values[0]

        )

    @flightApi.route("/use", methods=["POST"])
    def flightSearch():
        df = ds.datastore["aircraftStats"]["aircraftStatsDf"]
        aircraft = df[df["aircraft"].str.contains(request.args["aircraft"], regex=False)]
        runway = aircraft["minRunway"].values[0]
        searchParams = {
            "country": request.values["country"],
            "region": request.values["region"],
            "runway": runway,
            "rangemin": request.values["rangemin"],
            "rangemax": request.values["rangemax"],
            "city": request.values["city"]
        }
        ds.datastore["flightsList"]["searchParams"] = searchParams
        ds.getFlights()
        return redirect("/ae/flight?aircraft=" + request.args["aircraft"])

    return flightApi
