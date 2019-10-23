import api
from bs4 import BeautifulSoup
from getpass import getpass
import pandas as pd


# get password and login
username = input("Please enter username: ")
password = getpass()
# TODO wrong login
loginReq = api.login(username, password)


# get world to join
worldReq, airlineDf = api.getWorld(loginReq)
tryServer = True
while tryServer:
    airlineName = input("Please enter one of above mentioned airline names: ")
    # TODO Problem if airline has the same name on different server
    worldId = airlineDf[['worldId']].loc[airlineDf['name'] == airlineName].to_string(header=False, index=False).strip()
    userId = airlineDf[['userId']].loc[airlineDf['name'] == airlineName].to_string(header=False, index=False).strip()
    if ('Empty DataFrame' not in worldId and 'Empty DataFrame' not in userId):
        tryServer = False
    else:
        print("Airline does not exist, retry.")
gameServer = {
    "world": worldId,
    "userid": userId
}
print("entering world {} with {}".format(worldId, airlineName))


# enter world and get php session
phpSessidReq = requests.post(
    "http://www.airline-empires.com/index.php?app=ae&module=gameworlds&section=enterworld",
    cookies=worldReq.cookies,
    data=gameServer
)

# TODO not used
# go to airline mainpage
mainPageReq = requests.get("http://ae31.airline-empires.com/main.php", cookies=phpSessidReq.cookies)


# get all reachable airports from dep with args
# searchparams (create parser)
searchParams = {
    "country": "",
    "region": "",
    "runway": "4678",
    "rangenmin": "823",
    "rangemax": "1266",
    "city": "GZA"
}

print("getting all possible routes ...")
listFlightsReq = requests.get(
    "http://ae31.airline-empires.com/rentgate.php",
    params=searchParams,
    cookies=phpSessidReq.cookies
)
print("{:20} {:10} {:10} {:10}".format("Destination", "First", "Buisness","Economy"))
flightListPage = BeautifulSoup(listFlightsReq.text, 'html.parser')
flightList = flightListPage.findAll('tr')[2:]
for destination in flightList:
    routeDetailsUrl = destination.findAll('a')[1:][0].attrs['href']
    # getting flight details (demand)
    flightDetailsReq = requests.get(
        "http://ae31.airline-empires.com/" + routeDetailsUrl,
        cookies=phpSessidReq.cookies
    )

    routeDetailsPage = BeautifulSoup(flightDetailsReq.text, 'html.parser')
    highChartsScript = routeDetailsPage.findAll('script')[8:9][0].text
    rawData = re.findall(r"data: \[\d*,\d*,\d*\]", highChartsScript)[0]
    # demand format first, buisness, economy
    flightDemand = re.findall(r"\d*,\d*,\d*", rawData)[0].split(',')

    print("{:20} {:10} {:10} {:10}".format(
        destination.findAll('a')[0].text,
        flightDemand[0],
        flightDemand[1],
        flightDemand[2])
    )

    # get available aircrafts
    routeAircraftPostData = {
        "city1": searchParams["city"],
        "city2": destination.findAll('a')[0].text,
        "addflights": 1,
        "addflights_filter_actype": 0,
        "addflights_filter_hours": 1,
        "glairport": searchParams["city"],
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
    # Fix here, not selecting correct table
    availableAircraftsTable = availableAircraftsPage.findAll('table')[5:6][0]
    availableAircrafts = availableAircraftsTable.findAll('tr', recursive=False)[1:]

    # contains price and ifs
    flightInfo = availableAircraftsPage.findAll('table')[-1:][0]
    try:
        flightInfoPrices = flightInfo.contents[3].findAll('input')
    except:
        pass
    try:
        flightInfoIFS = flightInfo.contents[4].findAll('option')
    except:
        pass

    # TODO create dataframe with all the aircrafts and select the one with the best ratio
    for aircraft in availableAircrafts:
        try:
            maxAircraftFreq = aircraft.findAll('option')[-1:][0]
            try:
                firstAircraftPax = re.findall(r"\d* F", aircraft.text)[0].strip(' F')
            except IndexError as e:
                firstAircraftPax = 0
            try:
                buisnessAircraftPax = re.findall(r"\d* C", aircraft.text)[0].strip(' C')
            except IndexError as e:
                buisnessAircraftPax = 0
            try:
                economyAircraftPax = re.findall(r"\d* Y", aircraft.text)[0].strip(' Y')
            except IndexError as e:
                economyAircraftPax = 0

            reqFlightsList = []
            try:
                reqFlightsList.append(int(flightDemand[0])*7/int(firstAircraftPax))
            except ZeroDivisionError as e:
                reqFlightsList.append(0)
            try:
                reqFlightsList.append(int(flightDemand[1])*7/int(buisnessAircraftPax))
            except ZeroDivisionError as e:
                reqFlightsList.append(0)
            try:
                reqFlightsList.append(int(flightDemand[2])*7/int(economyAircraftPax))
            except ZeroDivisionError as e:
                reqFlightsList.append(0)

            reqFlights = math.ceil(max(reqFlightsList)+0.01)

            if reqFlights <= int(maxAircraftFreq.text):
                # add flight
                addFlightsPostData = {
                    "city1": searchParams["city"],
                    "city2": destination.findAll('a')[0].text,
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
                    "glairport": searchParams["city"],
                    "qty": 1
                }

                # Add plane and required frequency to post data
                aircraftId = aircraft.findAll('select')[0].attrs['name']
                addFlightsPostData[aircraftId] = reqFlights

                addFlightsReq = requests.post(
                    "http://ae31.airline-empires.com/route_details.php?city1={}&city2={}".format(
                        routeAircraftPostData['city1'],
                        routeAircraftPostData['city2']
                    ),
                    cookies=phpSessidReq.cookies,
                    data=addFlightsPostData
                )
                print("\tAdded {} flight(s)".format(reqFlights))
                break
        except:
            print("Aircraft not available")


# TODO when adding flights dont forget to check how many slots are avaiable and order additional or throw error message that the are no gates available

# sandbox
# soup = BeautifulSoup(worldPage.text,'html.parser')
with open("output.html", "w", encoding='utf-8') as file:
    file.write(str(worldList))



# TODO

# create api
# chose correct airplane
# auto lease gate / build terminal if possible
# fix ebl bug
# do not do duplicate flights
# split flights on multiple aircrafts (could be done with the dataframe of all aircrafts)

# parse error messages