import api
from getpass import getpass
import pandas as pd

flightRequestCsv = "flightRequest.csv"

flightRequestColumns = [
    "depAirport",
    "arrAirport",
    "flightDemandF",
    "flightDemandC",
    "flightDemandY",
]

try:
    flightRequestDf = pd.read_csv(flightRequestCsv, sep=";")
except FileNotFoundError as e:
    print(e)
    flightRequestDf = pd.DataFrame(columns=flightRequestColumns)

loginError = True
while loginError:
    # get password and login
    username = input("Please enter username: ")
    password = getpass()
    loginReq = api.login(username, password)

    # get world to join
    worldReq, airlineDf, loginError = api.get_world(loginReq)

tryServer = True
while tryServer:
    airlineName = input("Please enter one of above mentioned airline names: ")
    # TODO Problem if airline has the same name on different server
    worldId = (
        airlineDf[["worldId"]]
        .loc[airlineDf["name"] == airlineName]
        .to_string(header=False, index=False)
        .strip()
    )
    userId = (
        airlineDf[["userId"]]
        .loc[airlineDf["name"] == airlineName]
        .to_string(header=False, index=False)
        .strip()
    )
    if "Empty DataFrame" not in worldId and "Empty DataFrame" not in userId:
        tryServer = False
    else:
        print("Airline does not exist, retry.")
gameServer = {"world": worldId, "userid": userId}


# enter world
print("entering world {} with {}".format(worldId, airlineName))
phpSessidReq = api.enterWorld(worldReq, gameServer)


# get routes from departure airport
depAirportCode = input("Datamining start airport code: ")

searchParams = {
    "country": "",
    "region": "",
    "runway": "",
    "rangemin": "",
    "rangemax": "",
    "city": depAirportCode,
}

# get all reachable airports from dep with args
print("getting all possible routes from {}".format(depAirportCode))
listFlightsReq, flightsDf = api.get_flights(phpSessidReq, searchParams)
if not flightsDf.empty:
    print("Possible flights")
    print(flightsDf.to_string(index=False))

    print(
        "{:20} {:10} {:10} {:10}".format("Destination", "First", "Business", "Economy")
    )
    for idx, flight in flightsDf.iterrows():
        flightDemand = api.getFlightDemand(phpSessidReq, flight)
        flightDemandSeries = pd.Series(
            [
                depAirportCode,
                flight["airport"],
                flightDemand[0],
                flightDemand[1],
                flightDemand[2],
            ],
            index=flightRequestColumns,
        )
        flightRequestDf = flightRequestDf.append(flightDemandSeries, ignore_index=True)

flightRequestDf.to_csv(flightRequestCsv, sep=";", index=False)
