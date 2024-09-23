
import re
from typing import TYPE_CHECKING

import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Tag
from requests.models import Response

import cred
import userInput


if TYPE_CHECKING:
    pass


def tr_to_list(tr: Tag):
    row_list = []
    for td in tr:
        if td != '\n':
            row_list.append(td.text)
    return row_list


def get_request(url: str, cookies=None, params=None) -> tuple[Response , bool, str]:
    r = None
    request_error = True
    error_code = None
    try:
        r = requests.get(
            url=url,
            cookies=cookies,
            params=params,
            timeout=210
        )
        r.raise_for_status()
        request_error = False
    except requests.exceptions.Timeout as e:
        print("request timed-out")
        print(e)
    except requests.exceptions.ConnectionError as e:
        print("connection error")
        print(e)
    except requests.exceptions.HTTPError as e:
        error_code = r.status_code
        print(e)
    except requests.exceptions.ChunkedEncodingError as e:
        print("connection error")
        print(e)
    return r, request_error, error_code


def post_request(url: str, cookies: dict, data: dict):
    r = None
    request_error = True
    error_code = None
    try:
        r = requests.post(
            url,
            cookies=cookies,
            data=data,
            timeout=210
        )
        r.raise_for_status()
        request_error = False
    except requests.exceptions.Timeout as e:
        print("request timed-out")
        print(e)
    except requests.exceptions.ConnectionError as e:
        print("connection error")
        print(e)
    except requests.exceptions.HTTPError as e:
        error_code = r.status_code
        print(e)
    except requests.exceptions.ChunkedEncodingError as e:
        print("connection error")
        print(e)
    return r, request_error, error_code


def get_page_session():
    # get page session id
    session_request_error = True
    while session_request_error:
        print("Getting homepage cookies ...")
        forum_session_id_req, session_request_error, _ = get_request(
            url="http://www.airline-empires.com/index.php?/page/home.html"
        )
    return forum_session_id_req


def login(forum_session_id_req, username, password):
    login_request_error = True
    cred.user['ips_username'] = username
    cred.user['ips_password'] = password
    # do login
    while login_request_error:
        print("Logging in ...")
        login_request, login_request_error, _ = post_request(
            url="http://www.airline-empires.com/index.php?app=core&module=global&section=login&do=process",
            cookies=forum_session_id_req.cookies,
            data=cred.user
        )
    return login_request


def get_world(login_request):
    world_request_error = True
    airline_cols = [
        "worldName",
        "name",
        "idleAircraft",
        "DOP",
        "cash",
        "worldId",
        "userId"
    ]
    airline_df = pd.DataFrame(columns=airline_cols)

    # get worlds
    while world_request_error:
        worldReq, world_request_error, errorCode = get_request(
            url="http://www.airline-empires.com/index.php?app=ae",
            cookies=login_request.cookies
        )
        if (errorCode == 401):
            break

    if not world_request_error:
        print(f"logged in with user: {cred.user['ips_username']}")
        worldPage = BeautifulSoup(worldReq.text, 'html.parser')
        htmlWorldList = worldPage.find_all("div", "category_block block_wrap")
        for world in htmlWorldList:
            worldName = world.find("h3", "maintitle").text
            worldTable = world.find("table")
            airlinesTable = worldTable.find_all("tr", "row1")

            for airlineTable in airlinesTable:
                airlineName = airlineTable.find_all("td")[2].text.strip()
                airlineIdleAircraft = airlineTable.find_all("td")[5].text
                airlineDOP = airlineTable.find_all("td")[7].text
                airlineCash = airlineTable.find_all("td")[8].text
                airlineWorldId = airlineTable.find_all(
                    "input")[0].attrs['value'].strip()
                airlineUserId = airlineTable.find_all(
                    "input")[1].attrs['value'].strip()

                airline = pd.Series([
                    worldName,
                    airlineName,
                    airlineIdleAircraft,
                    airlineDOP,
                    airlineCash,
                    airlineWorldId,
                    airlineUserId
                ], index=airline_cols)
                airline_df = pd.concat([airline_df, airline.to_frame().T])

        print(airline_df.to_string(columns=[
            "worldName",
            "name",
            "idleAircraft",
            "DOP",
            "cash"
        ], index=False))

    return worldReq, airline_df, world_request_error


def do_login(forum_session_id_request, username: str, password: str):
    loginError = True
    while loginError:
        loginReq = login(forum_session_id_request, username, password)
        worldReq, airlineDf, loginError = get_world(loginReq)

    return worldReq, airlineDf

def enter_world(worldReq, gameServer):
    phpSessidReqError = True
    while phpSessidReqError:
        # enter world and get php session
        phpSessidReq, phpSessidReqError, _ = post_request(
            url="http://www.airline-empires.com/index.php?app=ae&module=gameworlds&section=enterworld",
            cookies=worldReq.cookies,
            data=gameServer
        )
    return phpSessidReq


def do_enter_world(world_name: str, airline_name: str, airline_df: pd.DataFrame, world_request):
    world_id = airline_df[['worldId']].loc[
        (airline_df["worldName"] == world_name) & (airline_df['name'] == airline_name)
    ].to_string(header=False, index=False).strip()
    user_id = airline_df[['userId']].loc[
        (airline_df["worldName"] == world_name) & (airline_df['name'] == airline_name)
    ].to_string(header=False, index=False).strip()

    game_server = {
        "world": world_id,
        "userid": user_id
    }

    php_session_id_request = enterWorld(world_request, game_server)
    return php_session_id_request

def enterWorld(worldReq, gameServer):
    phpSessidReqError = True
    while phpSessidReqError:
        # enter world and get php session
        phpSessidReq, phpSessidReqError, _ = post_request(
            url="http://www.airline-empires.com/index.php?app=ae&module=gameworlds&section=enterworld",
            cookies=worldReq.cookies,
            data=gameServer
        )
    return phpSessidReq


def doEnterWorld(args, airlineDf, worldReq):
    tryServer = True
    while tryServer:
        airlineName = userInput.setVar(
            args, "airline", "Please enter one of above mentioned airline names: ")
        # TODO Problem if airline has the same name on different server
        worldId = airlineDf[['worldId']].loc[airlineDf['name'] ==
                                             airlineName].to_string(header=False, index=False).strip()
        userId = airlineDf[['userId']].loc[airlineDf['name'] == airlineName].to_string(
            header=False, index=False).strip()
        if ('Empty DataFrame' not in worldId and 'Empty DataFrame' not in userId):
            tryServer = False
        else:
            print("Airline does not exist, retry.")
    gameServer = {
        "world": worldId,
        "userid": userId
    }

    # enter world
    print(f"entering world {worldId} with {airlineName}")
    phpSessidReq = enterWorld(worldReq, gameServer)
    return phpSessidReq


def get_aircraft_stats(session_id: str):
    mainPageReqError = True
    getAircraftsReqError = True
    aircraftStatsCol = [
        "aircraft",
        "range",
        "min_runway"
    ]
    aircraftStatsDf = pd.DataFrame(columns=aircraftStatsCol)

    while mainPageReqError:
        mainPageReq, mainPageReqError, _ = get_request(
            url="http://ae31.airline-empires.com/main.php",
            cookies={"PHPSESSID": session_id}
        )
    mainPage = BeautifulSoup(mainPageReq.text, 'lxml')
    airlineDetailsHref = mainPage.find(
        'a', text="Airline Details").attrs['href']

    while getAircraftsReqError:
        getAircraftsReq, getAircraftsReqError, _ = get_request(
            url=("http://ae31.airline-empires.com/" + airlineDetailsHref),
            cookies={"PHPSESSID": session_id}
        )

    aircraftListPage = BeautifulSoup(getAircraftsReq.text, 'lxml')
    aircraftHrefList = aircraftListPage.find_all(
        "a", href=re.compile(r'acdata.php\?aircraft*'))
    dedupAircraftHrefList = list(dict.fromkeys(aircraftHrefList))

    for aircraftHref in dedupAircraftHrefList:
        aircraftDetailReqError = True

        while aircraftDetailReqError:
            getAircraftDetailReq, aircraftDetailReqError, _ = get_request(
                url=("http://ae31.airline-empires.com/" +
                     aircraftHref.attrs['href']),
                cookies={"PHPSESSID": session_id}
            )

        aircraftDetailPage = BeautifulSoup(getAircraftDetailReq.text, 'lxml')
        aircraftName = aircraftDetailPage.find_all("div", class_="pagetitle")[
            0].text.replace(" Aircraft Information", '')
        engineInfoTable = aircraftDetailPage.find_all("table")[-1]

        maxRangeEngineSeries = pd.Series(['', 0, 0], index=aircraftStatsCol)
        for tr in engineInfoTable.find_all('tr')[1:]:
            engineTableRow = tr_to_list(tr)
            engineRange = int(
                re.sub(r' mi.*', '', engineTableRow[7]).replace(',', ''))
            engineMinRunway = int(engineTableRow[9].replace(',', ''))

            aircraftStats = pd.Series([
                aircraftName,
                engineRange,
                engineMinRunway
            ], index=aircraftStatsCol)

            if maxRangeEngineSeries['range'] < aircraftStats['range']:
                maxRangeEngineSeries = aircraftStats
        aircraftStatsDf = pd.concat(
            [aircraftStatsDf, maxRangeEngineSeries.to_frame().T])
    return aircraftStatsDf


def getFlights(session_id: str, searchParams: str):
    listFlightsReqError = True
    slotsRegex = r"\((\d*).*\)"
    flightsCols = [
        "airport",
        "flightUrl",
        "flightCreated",
        "slots",
        "gatesAvailable"
    ]
    flightsDf = pd.DataFrame(columns=flightsCols)

    while listFlightsReqError:
        listFlightsReq, listFlightsReqError, _ = get_request(
            url="http://ae31.airline-empires.com/rentgate.php",
            cookies={"PHPSESSID": session_id},
            params=searchParams
        )
    flightListPage = BeautifulSoup(listFlightsReq.text, 'html.parser')
    flightListTable = flightListPage.find_all("form")[1]
    flightList = flightListTable.find_all("tr")[1:]
    for flightRow in flightList:
        airport = flightRow.find_all("td")[0].text
        try:
            flightUrl = flightRow.find_all("td")[5].find("a").attrs['href']
        except AttributeError as e:
            print("Flight from {} to {} cannot be researched".format(
                searchParams["city"], airport))
            print(e)
        else:
            if (flightRow.find_all("td")[5].find("div") == None):
                flightCreated = False
            else:
                flightCreated = True
            try:
                slots = re.search(
                    slotsRegex, flightRow.find_all("td")[6].text).group(1)
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
            flightsDf = pd.concat([flightsDf, flight.to_frame().T])
    return listFlightsReq, flightsDf


def getFlightDemand(session_id: str, flight):
    if (re.match(r"\w{3}", flight['airport']) != None):
        flightDetailsReqError = True
        while flightDetailsReqError:
            # flight details
            flightDetailsReq, flightDetailsReqError, _ = get_request(
                url="http://ae31.airline-empires.com/" + flight['flightUrl'],
                cookies={"PHPSESSID": session_id},
            )
        routeDetailsPage = BeautifulSoup(flightDetailsReq.text, 'html.parser')
        highChartsScript = str(routeDetailsPage.findAll('script')[10])
        rawData = re.findall(r"data: \[\d*,\d*,\d*\]", highChartsScript)[0]
        flightDemand = [int(x) for x in re.findall(
            r"\d*,\d*,\d*", rawData)[0].split(',')]
        print()
        print("{:20} {:10} {:10} {:10}".format(
            flight['airport'],
            flightDemand[0],
            flightDemand[1],
            flightDemand[2])
        )
    else:
        flightDemand = [0, 0, 0]
    return flightDemand


def createFlight(session_id: str, depAirportCode, aircraftTypeFilter, reducedCapacityFlag, autoSlots, autoTerminal, minFreq, maxFreq, flight):
    availableAircraftsReqError = True
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

    flightDemand = getFlightDemand(session_id, flight)

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

    while availableAircraftsReqError:
        # look for available aircraft
        # post data required in order to see all available aircraft
        availableAircraftsReq, availableAircraftsReqError, _ = post_request(
            url="http://ae31.airline-empires.com/route_details.php?city1={}&city2={}".format(
                routeAircraftPostData['city1'],
                routeAircraftPostData['city2']
            ),
            cookies={"PHPSESSID": session_id},
            data=routeAircraftPostData
        )
    availableAircraftsPage = BeautifulSoup(
        availableAircraftsReq.text, 'html.parser')
    newFlightsPage = availableAircraftsPage.find("div", {"id": "newflights"})
    availableAircraftsTable = newFlightsPage.find(
        "td", text="Type").parent.parent.find_all("tr", recursive=False)[1:]

    for availableAircraftRow in availableAircraftsTable:
        aircraftData = availableAircraftRow.find_all('td', recursive=False)
        if (aircraftData[0].text == 'You do not have any aircraft available to serve this route.'):
            print(
                "You do not have any aircraft available to serve this route. (May also be a bug in AE code)")
        else:
            frequency = aircraftData[0].find_all('option')[-1:][0].text
        aircraftId = aircraftData[1].text
        aircraftType = aircraftData[2].text
        try:
            seatF = int(aircraftData[3].find_all(
                'td')[-3:-2][0].text.strip(' F'))
        except IndexError:
            seatF = 0
        try:
            seatC = int(aircraftData[3].find_all(
                'td')[-2:-1][0].text.strip(' C'))
        except IndexError:
            seatC = 0
        try:
            seatY = int(aircraftData[3].find_all(
                'td')[-1:][0].text.strip(' Y'))
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
        availableAircraftsDf = pd.concat([availableAircraftsDf, aircraft.to_frame().T])

    # type conversion
    availableAircraftsDf['frequency'] = availableAircraftsDf['frequency'].astype(
        int)
    availableAircraftsDf['seatF'] = availableAircraftsDf['seatF'].astype(int)
    availableAircraftsDf['seatC'] = availableAircraftsDf['seatC'].astype(int)
    availableAircraftsDf['seatY'] = availableAircraftsDf['seatY'].astype(int)
    availableAircraftsDf['hours'] = availableAircraftsDf['hours'].astype(int)

    # find correct aircraft
    if (aircraftTypeFilter != ''):
        availableAircraftsDf = availableAircraftsDf.loc[availableAircraftsDf['type']
                                                        == aircraftTypeFilter]
        if availableAircraftsDf.empty:
            print("No aircraft of this type available for this route")
    if (reducedCapacityFlag == 'n'):
        availableAircraftsDf = availableAircraftsDf.loc[availableAircraftsDf['reducedCapacity'] == False]
        if availableAircraftsDf.empty:
            print("No aircraft available for this route")

    # find required frequency compared to the demand
    flightDemandSeries = pd.Series(
        flightDemand, index=['seatReqF', 'seatReqC', 'seatReqY'])
    flightDemandSeries = flightDemandSeries*7
    availableAircraftsDf['seatReqF'] = flightDemandSeries['seatReqF']
    availableAircraftsDf['seatReqC'] = flightDemandSeries['seatReqC']
    availableAircraftsDf['seatReqY'] = flightDemandSeries['seatReqY']
    availableAircraftsDf['freqF'] = availableAircraftsDf['seatReqF'] / \
        availableAircraftsDf['seatF']
    availableAircraftsDf['freqC'] = availableAircraftsDf['seatReqC'] / \
        availableAircraftsDf['seatC']
    availableAircraftsDf['freqY'] = availableAircraftsDf['seatReqY'] / \
        availableAircraftsDf['seatY']
    availableAircraftsDf = availableAircraftsDf.replace(
        [np.inf, -np.inf], np.nan)
    availableAircraftsDf['avgFreq'] = availableAircraftsDf[[
        'freqF', 'freqC', 'freqY']].mean(axis=1) + 0.5
    # availableAircraftsDf[['avgFreq']].loc[availableAircraftsDf['avgFreq'] < availableAircraftsDf['freqY']](availableAircraftsDf[['freqY']].loc[availableAircraftsDf['avgFreq'] < availableAircraftsDf['freqY']])
    availableAircraftsDf['avgFreq'] = availableAircraftsDf['avgFreq'].apply(
        np.ceil)

    # get prices and ifs
    flightInfo = newFlightsPage.find('div', 'prices')
    if flightInfo is not None:
        flightInfo = flightInfo.contents[0]
        flightInfoPrices = []
        try:
            for allFlightPrices in flightInfo.contents[3].findAll('input'):
                flightInfoPrices.append(allFlightPrices.attrs['value'])
        except:
            pass

        flightInfoIFS = []
        try:
            for allFlightIFS in flightInfo.contents[4].findAll('option'):
                try:
                    allFlightIFS.attrs['selected']
                    flightInfoIFS.append(allFlightIFS.attrs['value'])
                except KeyError:
                    pass
        except:
            for allFlightIFS in flightInfo.find_all("a"):
                flightInfoIFS.append(
                    allFlightIFS.attrs['href'].split('id=')[-1:][0])

        # find planes to use
        availableAircraftsDf = availableAircraftsDf.sort_values('hours')
        if not availableAircraftsDf.empty:
            print(availableAircraftsDf)
        totPassengerY = 0
        totFreq = 0
        addFlightsPostData = {
            "city1": depAirportCode,
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
            "glairport": depAirportCode,
            "qty": 1
        }
        for _, availableAircraftRow in availableAircraftsDf.iterrows():
            minFreqCheck = True
            maxFreqCheck = True

            if (minFreq != ''):
                if (availableAircraftRow['avgFreq'] < int(minFreq)):
                    minFreqCheck = False
                    print("\t{} exceeded min defined frequency. No flights were added".format(
                        availableAircraftRow['type']))
                    if (aircraftTypeFilter != ''):
                        break
            if (maxFreq != ''):
                if (availableAircraftRow['avgFreq'] > int(maxFreq)):
                    maxFreqCheck = False
                    print("\t{} exceeded max defined frequency. No flights were added".format(
                        availableAircraftRow['type']))
                    if (aircraftTypeFilter != ''):
                        break

            if minFreqCheck and maxFreqCheck:
                if (availableAircraftRow['frequency'] >= availableAircraftRow['avgFreq']):
                    # case when required frequency less than available
                    addFlightsPostData["freq_" + availableAircraftRow['aircraft']
                                       ] = availableAircraftRow['avgFreq']

                    # check slots
                    oriSlotsAvailable = checkOriSlots(
                        session_id,
                        autoSlots,
                        autoTerminal,
                        depAirportCode
                    )

                    tgtSlotsAvailable = checkTgtSlots(
                        session_id,
                        autoSlots,
                        autoTerminal,
                        flight['airport'],
                        flight['slots'],
                        availableAircraftRow['avgFreq'],
                        flight['gatesAvailable']
                    )

                    if oriSlotsAvailable & tgtSlotsAvailable:
                        # add flight
                        addFlight(
                            session_id,
                            routeAircraftPostData['city1'],
                            routeAircraftPostData['city2'],
                            addFlightsPostData,
                            availableAircraftRow['avgFreq']
                        )
                    break
                else:
                    if ((totFreq + availableAircraftRow['frequency']) > availableAircraftRow['avgFreq']):
                        # case when enough flights were added
                        addFlightsPostData["freq_" + availableAircraftRow['aircraft']] = (
                            availableAircraftRow['avgFreq'] - totFreq)
                        totFreq += (availableAircraftRow['avgFreq'] - totFreq)
                    else:
                        # continue adding flights
                        addFlightsPostData["freq_" + availableAircraftRow['aircraft']
                                           ] = availableAircraftRow['frequency']
                        totFreq += availableAircraftRow['frequency']
                    totPassengerY += (availableAircraftRow['seatY']
                                      * availableAircraftRow['frequency'])
                    # check if the demand is meat (only checks Economy)
                    if (totPassengerY >= flightDemandSeries['seatReqY']):

                        # check slots, see func
                        oriSlotsAvailable = checkOriSlots(
                            session_id,
                            autoSlots,
                            autoTerminal,
                            depAirportCode
                        )

                        tgtSlotsAvailable = checkTgtSlots(
                            session_id,
                            autoSlots,
                            autoTerminal,
                            flight['airport'],
                            flight['slots'],
                            availableAircraftRow['avgFreq'],
                            flight['gatesAvailable']
                        )

                        if oriSlotsAvailable & tgtSlotsAvailable:
                            # add flight
                            addFlight(
                                session_id,
                                routeAircraftPostData['city1'],
                                routeAircraftPostData['city2'],
                                addFlightsPostData,
                                totFreq
                            )
                        break
    else:
        print("Error in page (no flights dispayed / available)")


def checkOriSlots(session_id: str, autoSlots, autoTerminal, airport):
    mainPageReqError = True
    gateUtilisationReqError = True
    getTerminalsReqError = True
    addTerminalReqError = True
    slotsAvailable = True

    while mainPageReqError:
        mainPageReq, mainPageReqError, _ = get_request(
            url="http://ae31.airline-empires.com/main.php",
            cookies={"PHPSESSID": session_id}
        )
    mainPage = BeautifulSoup(mainPageReq.text, 'html.parser')
    airlineDetailsHref = mainPage.find(
        'a', text="Airline Details").attrs['href']

    while gateUtilisationReqError:
        gateUtilisationReq, gateUtilisationReqError, _ = get_request(
            url=("http://ae31.airline-empires.com/" + airlineDetailsHref),
            cookies={"PHPSESSID": session_id}
        )
    gateUtilisationPage = BeautifulSoup(gateUtilisationReq.text, 'lxml')
    # TODO implement part when there is no bought slot from this airport
    gateUtilisationTable = gateUtilisationPage.find(id='airline_airport_list')
    gateTableHeaders = tr_to_list(
        gateUtilisationTable.find_all('tr')[0].findAll('td'))
    gateTableRowList = []
    for tr in gateUtilisationTable.find_all('tr')[1:]:
        gateTableRow = tr_to_list(tr)
        gateTableRowList.append(dict(zip(gateTableHeaders, gateTableRow)))
    gateUtilisationDf = pd.DataFrame(gateTableRowList)
    gateUtilisationDf = gateUtilisationDf.astype(
        dict(zip(gateTableHeaders, ['str', 'str', 'int', 'str'])))
    gateAmount = gateUtilisationDf.loc[gateUtilisationDf['Code']
                                       == airport]['Gates'] + 5
    gateUtilisation = int(gateUtilisationDf.loc[gateUtilisationDf['Code'] == airport]['Utilization'].to_string(
        index=False).lstrip().split('%')[0])

    # Terminal buying threshold
    if (gateUtilisation >= 80):
        slotsAvailable = False
        if (autoTerminal == 'y'):
            while getTerminalsReqError:
                getTerminalReq, getTerminalsReqError, _ = get_request(
                    url="http://ae31.airline-empires.com/termmarket.php",
                    cookies={"PHPSESSID": session_id}
                )
            getTerminalPage = BeautifulSoup(getTerminalReq.text, 'html.parser')
            buildTerminalData = {
                "qty": gateAmount,
                "id": airport,
                "price": "0",
                "action": "go"
            }
            while addTerminalReqError:
                _, addTerminalReqError, _ = get_request(
                    url="http://ae31.airline-empires.com/buildterm.php",
                    cookies={"PHPSESSID": session_id},
                    params=buildTerminalData
                )
            slotsAvailable = True
        else:
            print(
                "Automatically buy termial option is off. Flight may not be created due to slot restrictions!")
    return slotsAvailable


def checkTgtSlots(session_id, autoSlots, autoTerminal, airport, airportSlots, flightReqSlots, gatesAvailable):
    addSlotsReqError = True
    getTerminalsReqError = True
    addTerminalReqError = True
    slotsAvailable = True
    try:
        airportSlots = int(airportSlots)
    except TypeError:
        airportSlots = 0
    # check if there is enought slots, else buy some
    # +2 is to force to buy new slots / terminal when its almost full
    # because the termmarket page does not display terminal used at 100%
    # and passing from correct page would require a lot of request
    if (airportSlots < (flightReqSlots+2)):
        slotsAvailable = False
        # check if auto slot is on
        if (autoSlots == 'y'):
            if gatesAvailable:
                slotsLeaseData = {
                    "quicklease": "Lease 1 {}".format(airport)
                }
                while addSlotsReqError:
                    _, addSlotsReqError, _ = post_request(
                        url="http://ae31.airline-empires.com/rentgate.php",
                        cookies={"PHPSESSID": session_id},
                        data=slotsLeaseData
                    )
                slotsAvailable = True
            else:
                if (autoTerminal == 'y'):
                    while getTerminalsReqError:
                        getTerminalReq, getTerminalsReqError, _ = get_request(
                            url="http://ae31.airline-empires.com/termmarket.php",
                            cookies={"PHPSESSID": session_id}
                        )
                    getTerminalPage = BeautifulSoup(
                        getTerminalReq.text, 'html.parser')
                    # Not safe, redo
                    try:
                        gateAmount = int(getTerminalPage.find(
                            text=airport).next.next.next) + 5
                    except AttributeError:
                        gateAmount = 5
                    buildTerminalData = {
                        "qty": gateAmount,
                        "id": airport,
                        "price": "0",
                        "action": "go"
                    }
                    while addTerminalReqError:
                        _, addTerminalReqError, _ = get_request(
                            url="http://ae31.airline-empires.com/buildterm.php",
                            cookies={"PHPSESSID": session_id},
                            params=buildTerminalData
                        )
                    slotsAvailable = True
                else:
                    print("No slots available, buy terminal instead")
                slotsAvailable = False
    return slotsAvailable


def addHub(session_id: str, airport):
    addTerminalReqError = True
    addHubReqError = True
    buildTerminalData = {
        "qty": "5",
        "id": airport,
        "price": "0",
        "action": "go"
    }
    while addTerminalReqError:
        _, addTerminalReqError, _ = get_request(
            url="http://ae31.airline-empires.com/buildterm.php",
            cookies={"PHPSESSID": session_id},
            params=buildTerminalData
        )

    addHubData = {
        "hub": airport,
        "hubaction": "Open+Hub"
    }
    while addHubReqError:
        _, addHubReqError, _ = get_request(
            url="http://ae31.airline-empires.com/newhub.php",
            cookies={"PHPSESSID": session_id},
            params=addHubData
        )


def addFlight(session_id, city1, city2, addFlightsPostData, frequency):
    addFlightsReqError = True
    while addFlightsReqError:
        _, addFlightsReqError, _ = post_request(
            url="http://ae31.airline-empires.com/route_details.php?city1={}&city2={}".format(
                city1,
                city2
            ),
            cookies={"PHPSESSID": session_id},
            data=addFlightsPostData
        )
    print("\tAdded {} flight(s)".format(int(frequency)))


def getRoutes(session_id, startIdx):
    routesCols = [
        "routeId",
        "city1",
        "city2",
        "distance",
        "frequency",
        "loadFactorF",
        "loadFactorC",
        "loadFactorY",
        "priceF",
        "priceC",
        "priceY",
        "profit",
        "details"
    ]
    routesDf = pd.DataFrame(columns=routesCols)

    getRoutesReqError = True
    while getRoutesReqError:
        getRoutesReq, getRoutesReqError, _ = get_request(
            url="http://ae31.airline-empires.com/routes.php?city=all&order=desc&arr_dep=all&next={}".format(
                startIdx),
            cookies={"PHPSESSID": session_id}
        )
    getRoutesPage = BeautifulSoup(getRoutesReq.text, 'html.parser')
    routes = getRoutesPage.find_all("form", id="routes")
    for route in routes:
        routeInfos = route.find_all("td")
        routeId = routeInfos[0].find("input").attrs['id']
        city1 = routeInfos[2].find_all("a")[0].text
        city2 = routeInfos[2].find_all("a")[1].text
        distance = routeInfos[3].text
        frequency = routeInfos[4].text.split("x Weekly")[0]
        try:
            loadFactorF = re.findall(r'\D*(\d+)\D*', routeInfos[5].text)[0]
        except IndexError:
            loadFactorF = np.nan
        try:
            loadFactorC = re.findall(r'\D*(\d+)\D*', routeInfos[6].text)[0]
        except IndexError:
            loadFactorC = np.nan
        try:
            loadFactorY = re.findall(r'\D*(\d+)\D*', routeInfos[7].text)[0]
        except IndexError:
            loadFactorY = np.nan
        try:
            priceF = re.findall(r'\D*(\d+)\D*', routeInfos[8].text)[0]
        except IndexError:
            priceF = np.nan
        try:
            priceC = re.findall(r'\D*(\d+)\D*', routeInfos[9].text)[0]
        except IndexError:
            priceC = np.nan
        try:
            priceY = re.findall(r'\D*(\d+)\D*', routeInfos[10].text)[0]
        except IndexError:
            priceY = np.nan
        profit = re.findall(r'[^-]?(-?\d+)\D*', routeInfos[11].text)[0]
        details = routeInfos[12].find("a").attrs['href']
        routeSeries = pd.Series([
            routeId,
            city1,
            city2,
            distance,
            frequency,
            loadFactorF,
            loadFactorC,
            loadFactorY,
            priceF,
            priceC,
            priceY,
            profit,
            details
        ], index=routesCols)
        routesDf = pd.concat([routesDf, routeSeries.to_frame().T])
    return routesDf


def closeRoutes(session_id, routesDf):
    closeRoutesData = {
        "checkedroutes[]": [],
        "routeaction": "close",
        "closeroute": "close",
        "massact": "go"
    }
    for _, route in routesDf.iterrows():
        closeRoutesData['checkedroutes[]'].append(route['routeId'])
    closeRoutesReqError = True
    while closeRoutesReqError:
        _, closeRoutesReqError, _ = post_request(
            url="http://ae31.airline-empires.com/routes.php",
            cookies={"PHPSESSID": session_id},
            data=closeRoutesData
        )
