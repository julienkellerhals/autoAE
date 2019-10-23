import requests
from bs4 import BeautifulSoup
import re
import math
import cred
import pandas as pd
import numpy as np

# get page session id
print("Getting homepage cookies ...")
forumSessidReq = requests.get("http://www.airline-empires.com/index.php?/page/home.html")

def login(username, password):
    cred.user['ips_username'] = username
    cred.user['ips_password'] = password
    # do login
    print("Logging in ...")
    loginReq = requests.post(
        "http://www.airline-empires.com/index.php?app=core&module=global&section=login&do=process",
        cookies=forumSessidReq.cookies,
        data=cred.user
    )
    print("logged in with user: {}".format(cred.user['ips_username']))
    return loginReq

def getWorld(loginReq):
    airlineCols = [
        "worldName",
        "name",
        "idleAircraft",
        "DOP",
        "cash",
        "worldId",
        "userId"
    ]
    airlineDf = pd.DataFrame(columns=airlineCols)
    # get worlds
    print("getting all worlds ...")
    worldReq = requests.get(
        "http://www.airline-empires.com/index.php?app=ae",
        cookies=loginReq.cookies,
    )
    worldPage = BeautifulSoup(worldReq.text, 'html.parser')
    htmlWorldList = worldPage.find_all("div","category_block block_wrap")
    for world in htmlWorldList:
        worldName = world.find("h3","maintitle").text
        worldTable = world.find("table")
        airlinesTable = worldTable.find_all("tr", "row1")
        for airlineTable in airlinesTable:
            airlineName = airlineTable.find_all("td")[2].text.strip()
            airlineIdleAircraft = airlineTable.find_all("td")[5].text
            airlineDOP = airlineTable.find_all("td")[7].text
            airlineCash = airlineTable.find_all("td")[8].text
            airlineWorldId = airlineTable.find_all("input")[0].attrs['value'].strip()
            airlineUserId = airlineTable.find_all("input")[1].attrs['value'].strip()
            airline = pd.Series([
                worldName,
                airlineName,
                airlineIdleAircraft,
                airlineDOP,
                airlineCash,
                airlineWorldId,
                airlineUserId
            ], index=airlineCols)
            airlineDf = airlineDf.append(airline, ignore_index=True)
    print(airlineDf.to_string(columns=[
        "worldName",
        "name",
        "idleAircraft",
        "DOP",
        "cash"
    ], index=False))
    return worldReq, airlineDf

def enterWorld(worldReq, gameServer):
    # enter world and get php session
    phpSessidReq = requests.post(
        "http://www.airline-empires.com/index.php?app=ae&module=gameworlds&section=enterworld",
        cookies=worldReq.cookies,
        data=gameServer
    )
    return phpSessidReq

def getFlights(phpSessidReq, searchParams):
    slotsRegex = r"\((\d*).*\)"
    flightsCols = [
        "airport",
        "flightUrl",
        "flightCreated",
        "slots",
        "gatesAvailable"
    ]
    flightsDf = pd.DataFrame(columns=flightsCols)

    listFlightsReq = requests.get(
        "http://ae31.airline-empires.com/rentgate.php",
        params=searchParams,
        cookies=phpSessidReq.cookies
    )
    flightListPage = BeautifulSoup(listFlightsReq.text, 'html.parser')
    flightListTable = flightListPage.find_all("form")[1]
    flightList = flightListTable.find_all("tr")[1:]
    for flightRow in flightList:
        airport = flightRow.find_all("td")[0].text
        flightUrl = flightRow.find_all("td")[5].find("a").attrs['href']
        if (flightRow.find_all("td")[5].find("div") == None):
            flightCreated = False
        else:
            flightCreated  = True    
        try:
            slots = re.search(slotsRegex, flightRow.find_all("td")[6].text).group(1)
        except AttributeError:
            slots = None
        if (flightRow.find_all("td")[10].find("input") == None):
            gatesAvailable = False
        else:
            gatesAvailable = True
        flight = pd.Series([
            airport,
            flightUrl,
            flightCreated,
            slots,
            gatesAvailable
        ], index=flightsCols)
        flightsDf = flightsDf.append(flight, ignore_index=True)
    return listFlightsReq, flightsDf

def createFlight(phpSessidReq, depAirportCode, aircraftTypeFilter, reducedCapacityFlag, flight):
    availableAircraftsCols = [
        "frequency",
        "aircraft",
        "type",
        "seatF",
        "seatC",
        "seatY",
        "reducedCapacity",
        "hours"
    ]
    availableAircraftsDf = pd.DataFrame(columns=availableAircraftsCols)

    # flight details
    flightDetailsReq = requests.get(
        "http://ae31.airline-empires.com/" + flight['flightUrl'],
        cookies=phpSessidReq.cookies
    )
    routeDetailsPage = BeautifulSoup(flightDetailsReq.text, 'html.parser')
    highChartsScript = routeDetailsPage.findAll('script')[8:9][0].text
    rawData = re.findall(r"data: \[\d*,\d*,\d*\]", highChartsScript)[0]
    flightDemand = [int(x) for x in re.findall(r"\d*,\d*,\d*", rawData)[0].split(',')]
    [ int(x) for x in "40 1".split(" ") ]
    print()
    print("{:20} {:10} {:10} {:10}".format(
        flight['airport'],
        flightDemand[0],
        flightDemand[1],
        flightDemand[2])
    )

    # aircraft details
    routeAircraftPostData = {
        "city1": depAirportCode,
        "city2": flight['airport'],
        "addflights": 1,
        "addflights_filter_actype": 0,
        "addflights_filter_hours": 1,
        "glairport": depAirportCode,
        "qty": 1
    }

    # look for available aircrafts
    # post data required in order to see all available aricrafts
    availableAircraftsReq = requests.post(
        "http://ae31.airline-empires.com/route_details.php?city1={}&city2={}".format(
            routeAircraftPostData['city1'],
            routeAircraftPostData['city2']
        ),
        cookies=phpSessidReq.cookies,
        data=routeAircraftPostData
    )
    availableAircraftsPage = BeautifulSoup(availableAircraftsReq.text, 'html.parser')
    newFlightsPage = availableAircraftsPage.find("div", {"id": "newflights"})
    availableAircraftsTable = newFlightsPage.find("td",text="Type").parent.parent.find_all("tr", recursive=False)[1:]
    
    for availableAircraftRow in availableAircraftsTable:
        aircraftData = availableAircraftRow.find_all('td', recursive=False)
        if (aircraftData[0].text == 'You do not have any aircraft available to serve this route.'):
            break
        else:
            frequency = aircraftData[0].find_all('option')[-1:][0].text
        aircraftId = aircraftData[1].text
        aircraftType = aircraftData[2].text
        try:
            seatF = int(aircraftData[3].find_all('td')[-3:-2][0].text.strip(' F'))
        except IndexError:
            seatF = 0
        try:
            seatC = int(aircraftData[3].find_all('td')[-2:-1][0].text.strip(' C'))
        except IndexError:
            seatC = 0
        try:
            seatY = int(aircraftData[3].find_all('td')[-1:][0].text.strip(' Y'))
        except IndexError:
            seatY = 0
        if (aircraftData[4].find_all('span') == []):
            reducedCapacity = False
        else:
            reducedCapacity = True
        hours = aircraftData[5].text
        aircraft = pd.Series([
            frequency,
            aircraftId,
            aircraftType,
            seatF,
            seatC,
            seatY,
            reducedCapacity,
            hours
        ], index=availableAircraftsCols)
        availableAircraftsDf = availableAircraftsDf.append(aircraft, ignore_index=True)
    
    # type conversion
    availableAircraftsDf['frequency'] = availableAircraftsDf['frequency'].astype(int)
    availableAircraftsDf['seatF'] = availableAircraftsDf['seatF'].astype(int)
    availableAircraftsDf['seatC'] = availableAircraftsDf['seatC'].astype(int)
    availableAircraftsDf['seatY'] = availableAircraftsDf['seatY'].astype(int)
    availableAircraftsDf['hours'] = availableAircraftsDf['hours'].astype(int)

    # find correct aircraft
    if (aircraftTypeFilter != ''):
        availableAircraftsDf = availableAircraftsDf.loc[availableAircraftsDf['type'] == aircraftTypeFilter]
        if availableAircraftsDf.empty:
            print("No aircraft of this type available for this route")
    if (reducedCapacityFlag == 'n'):
        availableAircraftsDf = availableAircraftsDf.loc[availableAircraftsDf['reducedCapacity'] == False]
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
    availableAircraftsDf['avgFreq'] = availableAircraftsDf[['freqF','freqC','freqY']].mean(axis=1) + 1
    # availableAircraftsDf[['avgFreq']].loc[availableAircraftsDf['avgFreq'] < availableAircraftsDf['freqY']](availableAircraftsDf[['freqY']].loc[availableAircraftsDf['avgFreq'] < availableAircraftsDf['freqY']])
    availableAircraftsDf['avgFreq'] = availableAircraftsDf['avgFreq'].apply(np.ceil)

    # get prices and ifs
    flightInfo = newFlightsPage.findAll('table')[-1:][0]
    try:
        flightInfoPrices = flightInfo.contents[3].findAll('input')
    except:
        pass

    try:
        flightInfoIFS = []
        for allFlightIFS in flightInfo.contents[4].findAll('option'):
            try:
                allFlightIFS.attrs['selected']
                flightInfoIFS.append(allFlightIFS)
            except KeyError:
                pass
    except:
        pass

    # find planes to use
    availableAircraftsDf = availableAircraftsDf.sort_values('hours')
    print(availableAircraftsDf)
    totPassengerY = 0
    totFreq = 0
    addFlightsPostData = {
        "city1": depAirportCode,
        "city2": flight['airport'],
        "addflights": 1,
        "addflights_filter_actype": 0,
        "addflights_filter_hours": 1,
        "price_new_f": flightInfoPrices[0].attrs['value'],
        "price_new_c": flightInfoPrices[1].attrs['value'],
        "price_new_y": flightInfoPrices[2].attrs['value'],
        "ifs_id_f": flightInfoIFS[0].attrs['value'],
        "ifs_id_c": flightInfoIFS[1].attrs['value'],
        "ifs_id_y": flightInfoIFS[2].attrs['value'],
        "confirmaddflights": "Add Flights",
        "glairport": depAirportCode,
        "qty": 1
    }
    for idx, availableAircraftRow in availableAircraftsDf.iterrows():
        # add flight
        if (availableAircraftRow['frequency'] > availableAircraftRow['frequency']):
            addFlightsPostData["freq_" + availableAircraftRow['aircraft']] = availableAircraftRow['frequency']
            addFlightsReq = requests.post(
                "http://ae31.airline-empires.com/route_details.php?city1={}&city2={}".format(
                    routeAircraftPostData['city1'],
                    routeAircraftPostData['city2']
                ),
                cookies=phpSessidReq.cookies,
                data=addFlightsPostData
            )
            print("\tAdded {} flight(s)".format(availableAircraftRow['frequency']))
            break
        else:
            if ((totFreq + availableAircraftRow['frequency']) > availableAircraftRow['avgFreq']):
                addFlightsPostData["freq_" + availableAircraftRow['aircraft']] = (availableAircraftRow['avgFreq'] - totFreq)
                totFreq += (availableAircraftRow['avgFreq'] - totFreq)
            else:
                addFlightsPostData["freq_" + availableAircraftRow['aircraft']] = availableAircraftRow['frequency']
                totFreq += availableAircraftRow['frequency']
            totPassengerY += (availableAircraftRow['seatY'] * availableAircraftRow['frequency'])
            if (totPassengerY >= flightDemandSeries['seatReqY']):
                addFlightsReq = requests.post(
                    "http://ae31.airline-empires.com/route_details.php?city1={}&city2={}".format(
                        routeAircraftPostData['city1'],
                        routeAircraftPostData['city2']
                    ),
                    cookies=phpSessidReq.cookies,
                    data=addFlightsPostData
                )
                print("\tAdded {} flight(s)".format(totFreq))
                break
