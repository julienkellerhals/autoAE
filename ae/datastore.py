from datetime import datetime
import pandas as pd

from ae.aeRequest import AeRequest
from ae.pageParser import PageParser
from service.datastoreBase import datastoreBase

class Datastore():
    req: AeRequest = None
    parser: PageParser = None
    datastore: dict = {}

    def __init__(self) -> None:
        self.req = AeRequest()
        self.parser = PageParser()
        self.datastore = datastoreBase

    def login(self, username: str, password: str):
        user = {
            "auth_key": "880ea6a14ea49e853634fbdc5015a024",
            "ips_username": username,
            "ips_password": password
        }
        self.datastore["login"]["status"] = self.req.login(user)
        self.datastore["login"]["time"] = datetime.now()

    def getWorld(self):
        worldReq, worldReqError = self.req.getWorld()
        airlineDf = self.datastore["airlines"]["airlineDf"]
        airlineCols = self.datastore["airlines"]["airlineCols"]

        if not worldReqError:
            airlineDf = self.parser.getWorld(
                worldReq.text,
                airlineDf,
                airlineCols
            )
            self.datastore["airlines"]["airlineDf"] = airlineDf

    def enterWorld(self, worldId: str, userId: str):
        serverInfo = {
            "world": worldId,
            "userid": userId
        }
        self.req.enterWorld(serverInfo)

    def getAircraftStats(self):
        mainPageReq = self.req.getMainPage()
        airlineDetailsHref = self.parser.getAirlineDetails(mainPageReq.text)
        aircraftReq = self.req.getAircraft(airlineDetailsHref)
        aircraftList = self.parser.getAircraftList(aircraftReq.text)

        for aircraft in aircraftList:
            aircraftDetailsReq = self.req.getAircraftDetails(aircraft.attrs['href'])
            self.datastore["aircraftStats"]["aircraftStatsDf"] = self.parser.getAircraftDetails(
                aircraftDetailsReq.text,
                self.datastore["aircraftStats"]["aircraftStatsCols"],
                self.datastore["aircraftStats"]["aircraftStatsDf"],
            )

    def getFlights(self):
        flightListReq = self.req.getFlightList(self.datastore["flightsList"]["searchParams"])
        self.datastore["flightsList"]["flightsListDf"] = self.parser.getFlightList(
            flightListReq.text,
            self.datastore["flightsList"]["flightsListCols"],
            self.datastore["flightsList"]["flightsListDf"]
        )
