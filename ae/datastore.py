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

    def getAvailableFlights(self):
        flightsDf = self.datastore["flightsList"]["flightsListDf"]
        availableFlightsDf = flightsDf[
            ["airport","flightUrl","slots","gatesAvailable"]
        ].loc[flightsDf['flightCreated'] is False]
        return availableFlightsDf

    def createFlight(self):
        flightParams = self.datastore["flightsList"]["flightParams"]
        availableFlightsDf = self.getAvailableFlights()
        # if not availableFlightsDf.empty:

            # Add hub
            # TODO implement create route
            # if (flightParams["autoHub"] is True):
            #     addHub(phpSessidReq, depAirportCode)

            # print("{:20} {:10} {:10} {:10}".format(
            #         "Destination",
            #         "First",
            #         "Business",
            #         "Economy"
            # ))
            # for idx, flight in availableFlightsDf.iterrows():
            #     api.createFlight(
            #         phpSessidReq,
            #         depAirportCode,
            #         aircraftType,
            #         reducedCapacityFlag,
            #         autoSlots,
            #         autoTerminal,
            #         minFreq,
            #         maxFreq,
            #         flight
            #     )
        # else:
        #     print("No new flights available.")
