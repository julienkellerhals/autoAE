from datetime import datetime
import re
import numpy as np
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
        airlineCols = self.datastore["airlines"]["airlineCols"]

        if not worldReqError:
            airlineDf = self.parser.getWorld(
                worldReq.text,
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
        aircraftStatsCols = self.datastore["aircraftStats"]["aircraftStatsCols"]
        self.datastore["aircraftStats"]["aircraftStatsDf"] = pd.DataFrame(columns=aircraftStatsCols)

        mainPageReq = self.req.getMainPage()
        airlineDetailsHref = self.parser.getAirlineDetails(mainPageReq.text)
        aircraftReq = self.req.getAircraft(airlineDetailsHref)
        aircraftList = self.parser.getAircraftList(aircraftReq.text)

        for aircraft in aircraftList:
            aircraftDetailsReq = self.req.getAircraftDetails(aircraft.attrs['href'])
            self.datastore["aircraftStats"]["aircraftStatsDf"] = self.parser.getAircraftDetails(
                aircraftDetailsReq.text,
                aircraftStatsCols,
                self.datastore["aircraftStats"]["aircraftStatsDf"],
            )

    def getFlights(self):
        flightListReq = self.req.getFlightList(self.datastore["flightsList"]["searchParams"])
        self.datastore["flightsList"]["flightsListDf"] = self.parser.getFlightList(
            flightListReq.text,
            self.datastore["flightsList"]["flightsListCols"],
        )

    def getAvailableFlights(self):
        flightsDf = self.datastore["flightsList"]["flightsListDf"]
        availableFlightsDf = flightsDf[
            ["airport","flightUrl","slots","gatesAvailable"]
        ].loc[flightsDf['flightCreated'] == False]
        return availableFlightsDf

    def createFlights(self, aircraft: str):
        flightParams = self.datastore["flightsList"]["flightParams"]
        searchParams = self.datastore["flightsList"]["searchParams"]
        availableFlightsDf = self.getAvailableFlights()
        if not availableFlightsDf.empty:
            if flightParams["autoHub"] is True:
                self.req.createHub(searchParams["city"])

            print("{:20} {:10} {:10} {:10}".format(
                    "Destination",
                    "First",
                    "Business",
                    "Economy"
            ))
            for _, flight in availableFlightsDf.iterrows():
                self.createFlight(
                    flight,
                    aircraft,
                )
        else:
            print("No new flights available.")

    def createFlight(self, flight: pd.Series, aircraft: str):
        flightParams = self.datastore["flightsList"]["flightParams"]
        searchParams = self.datastore["flightsList"]["searchParams"]

        if re.match(r"\w{3}",flight['airport']) is not None:
            flightDetailsReq = self.req.getFlightDemand(flight['flightUrl'])
            flightDemand = self.parser.getFlightDemand(flightDetailsReq.text)
        else:
            flightDemand = [0,0,0]

        route = {
            "city1": searchParams["city"],
            "city2": flight['airport'],
            "addflights": 1,
            "addflights_filter_actype": 0,
            "addflights_filter_hours": 1,
            "glairport": searchParams["city"],
            "qty": 1
        }

        availableAircraftReq = self.req.getAvailableAircrafts(route)
        availableAircraftsDf = self.parser.getAvailableAircrafts(
            availableAircraftReq.text,
            self.datastore["flightsList"]["availableAircraftsCols"],
        )

        # type conversion
        availableAircraftsDf['frequency'] = availableAircraftsDf['frequency'].astype(int)
        availableAircraftsDf['seatF'] = availableAircraftsDf['seatF'].astype(int)
        availableAircraftsDf['seatC'] = availableAircraftsDf['seatC'].astype(int)
        availableAircraftsDf['seatY'] = availableAircraftsDf['seatY'].astype(int)
        availableAircraftsDf['hours'] = availableAircraftsDf['hours'].astype(int)

        # find correct aircraft
        if aircraft != '':
            availableAircraftsDf = availableAircraftsDf.loc[
                availableAircraftsDf['type'] == aircraft
            ]
            if availableAircraftsDf.empty:
                print("No aircraft of this type available for this route")

        if flightParams["reducedCap"] is False:
            availableAircraftsDf = availableAircraftsDf.loc[
                availableAircraftsDf['reducedCapacity'] == False
            ]
            if availableAircraftsDf.empty:
                print("No aircraft available for this route")

        # find required frequency compared to the demand
        flightDemandSeries = pd.Series(flightDemand, index=['seatReqF','seatReqC','seatReqY'])
        flightDemandSeries = flightDemandSeries*7
        availableAircraftsDf['seatReqF'] = flightDemandSeries['seatReqF']
        availableAircraftsDf['seatReqC'] = flightDemandSeries['seatReqC']
        availableAircraftsDf['seatReqY'] = flightDemandSeries['seatReqY']
        availableAircraftsDf['freqF'] = availableAircraftsDf['seatReqF'] / availableAircraftsDf['seatF']
        availableAircraftsDf['freqC'] = availableAircraftsDf['seatReqC'] / availableAircraftsDf['seatC']
        availableAircraftsDf['freqY'] = availableAircraftsDf['seatReqY'] / availableAircraftsDf['seatY']
        availableAircraftsDf = availableAircraftsDf.replace([np.inf, -np.inf], np.nan)
        availableAircraftsDf['avgFreq'] = availableAircraftsDf[['freqF','freqC','freqY']].mean(axis=1) + 0.5
        # availableAircraftsDf[['avgFreq']].loc[availableAircraftsDf['avgFreq'] < availableAircraftsDf['freqY']](availableAircraftsDf[['freqY']].loc[availableAircraftsDf['avgFreq'] < availableAircraftsDf['freqY']])
        availableAircraftsDf['avgFreq'] = availableAircraftsDf['avgFreq'].apply(np.ceil)

        flightInfo, flightInfoPrices, flightInfoIFS = self.parser.getFlightInfo(availableAircraftReq.text)

        if flightInfo is not None:
            # find planes to use
            availableAircraftsDf = availableAircraftsDf.sort_values('hours')
            if not availableAircraftsDf.empty:
                print(availableAircraftsDf)

            totPassengerY = 0
            totFreq = 0
            addFlightsPostData = {
                "city1": searchParams["city"],
                "city2": flight['airport'],
                "addflights": 1,
                "addflights_filter_actype": 0,
                "addflights_filter_hours": 1,
                "price_new_f": flightInfoPrices[0],
                "price_new_c": flightInfoPrices[1],
                "price_new_y": flightInfoPrices[2],
                "ifs_id_f": flightInfoIFS[0],
                "ifs_id_c": flightInfoIFS[1],
                "ifs_id_y": flightInfoIFS[2],
                "confirmaddflights": "Add Flights",
                "glairport": searchParams["city"],
                "qty": 1
            }
            for _, availableAircraftRow in availableAircraftsDf.iterrows():
                minFreqCheck = True
                maxFreqCheck = True

                if flightParams["minFreq"] != '':
                    if availableAircraftRow['avgFreq'] < int(flightParams["minFreq"]):
                        minFreqCheck = False
                        print("\t{} exceeded min defined frequency. No flights were added".format(availableAircraftRow['type']))
                        if aircraft != '':
                            break
                if flightParams["maxFreq"] != '':
                    if availableAircraftRow['avgFreq'] > int(flightParams["maxFreq"]):
                        maxFreqCheck = False
                        print("\t{} exceeded max defined frequency. No flights were added".format(availableAircraftRow['type']))
                        if aircraft != '':
                            break
                
                if minFreqCheck and maxFreqCheck:
                    if availableAircraftRow['frequency'] >= availableAircraftRow['avgFreq']:
                        # case when required frequency less than available
                        addFlightsPostData["freq_" + availableAircraftRow['aircraft']] = availableAircraftRow['avgFreq']

                        # check slots
                        oriSlotsAvailable = self.checkOriSlots(
                            flightParams["autoTerminal"],
                            searchParams["city"]
                        )

                        tgtSlotsAvailable = self.checkTgtSlots(
                            flightParams["autoSlots"],
                            flightParams["autoTerminal"],
                            flight['airport'],
                            flight['slots'],
                            availableAircraftRow['avgFreq'],
                            flight['gatesAvailable']
                        )

                        if oriSlotsAvailable & tgtSlotsAvailable:
                            # add flight
                            self.req.addFlight(
                                addFlightsPostData,
                                availableAircraftRow['avgFreq']
                            )
                        break
                    else:
                        if ((totFreq + availableAircraftRow['frequency']) > availableAircraftRow['avgFreq']):
                            # case when enough flights were added
                            addFlightsPostData["freq_" + availableAircraftRow['aircraft']] = (availableAircraftRow['avgFreq'] - totFreq)
                            totFreq += (availableAircraftRow['avgFreq'] - totFreq)
                        else:
                            # continue adding flights
                            addFlightsPostData["freq_" + availableAircraftRow['aircraft']] = availableAircraftRow['frequency']
                            totFreq += availableAircraftRow['frequency']
                        totPassengerY += (availableAircraftRow['seatY'] * availableAircraftRow['frequency'])
                        # check if the demand is meat (only checks Economy)
                        if (totPassengerY >= flightDemandSeries['seatReqY']):

                            # check slots, see func
                            oriSlotsAvailable = self.checkOriSlots(
                                flightParams["autoTerminal"],
                                searchParams["city"]
                            )

                            tgtSlotsAvailable = self.checkTgtSlots(
                                flightParams["autoSlots"],
                                flightParams["autoTerminal"],
                                flight['airport'],
                                flight['slots'],
                                availableAircraftRow['avgFreq'],
                                flight['gatesAvailable']
                            )

                            if oriSlotsAvailable & tgtSlotsAvailable:
                                # add flight
                                self.req.addFlight(
                                    addFlightsPostData,
                                    availableAircraftRow['avgFreq']
                                )
                            break
        else:
            print("Error in page (no flights dispayed / available)")

    def checkOriSlots(self, autoTerminal: str, airport: str):
        slotsAvailable = True

        mainPageReq = self.req.getMainPage()
        airlineDetailsHref = self.parser.getAirlineDetails(mainPageReq.text)
        gateUtilizationReq = self.req.getGateUtilization(airlineDetailsHref)
        gateUtilizationDf = self.parser.getGateUtilization(gateUtilizationReq.text)
        gateAmount = gateUtilizationDf.loc[gateUtilizationDf['Code'] == airport]['Gates'] + 5
        gateUtilization = int(gateUtilizationDf.loc[
            gateUtilizationDf['Code'] == airport.upper()
        ]['Utilization'].to_string(index=False).lstrip().split('%')[0])

        # Terminal buying threshold
        if gateUtilization >= 80:
            if autoTerminal is True:
                buildTerminalData = {
                    "qty": gateAmount,
                    "id": airport,
                    "price": "0",
                    "action": "go"
                }
                self.req.addTerminal(buildTerminalData)
                slotsAvailable = True
            else:
                slotsAvailable = False
                print(
                    "Automatically buy terminal option is off."
                    "Flight may not be created due to slot restrictions!"
                )
        return slotsAvailable

    def checkTgtSlots(
        self,
        autoSlots,
        autoTerminal,
        airport,
        airportSlots,
        flightReqSlots,
        gatesAvailable
    ):
        slotsAvailable = True

        try:
            airportSlots = int(airportSlots)
        except TypeError:
            airportSlots = 0
        # check if there is enough slots, else buy some
        # +2 is to force to buy new slots / terminal when its almost full
        # because the termmarket page does not display terminal used at 100%
        # and passing from correct page would require a lot of request
        if airportSlots < (flightReqSlots+2):
            slotsAvailable = False
            # check if auto slot is on
            if autoSlots is True:
                if gatesAvailable:
                    slotsLeaseData = {
                        "quicklease": "Lease 1 {}".format(airport)
                    }
                    self.req.addSlots(slotsLeaseData)
                    slotsAvailable = True
                else:
                    if autoTerminal is True:
                        getTerminalReq = self.req.getTerminal()
                        gateAmount = self.parser.getTerminal(getTerminalReq.text, airport)

                        buildTerminalData = {
                            "qty": gateAmount,
                            "id": airport,
                            "price": "0",
                            "action": "go"
                        }
                        self.req.addTerminal(buildTerminalData)
                        slotsAvailable = True
                    else:
                        slotsAvailable = False
                        print("No slots available, buy terminal instead")
        return slotsAvailable
