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


# enter world
print("entering world {} with {}".format(worldId, airlineName))
phpSessidReq = api.enterWorld(worldReq, gameServer)


# get routes from departure airport
flightCountry = input("Flight country: ")
flightRegion = input("Flight region: ")
requiredRunway = input("Minimum runway length: ")
rangeMin = input("Flight minimum range: ")
rangeMax = input("Flight maximum range: ")
depAirportCode = input("Departure airport code: ")

searchParams = {
    "country": flightCountry,
    "region": flightRegion,
    "runway": requiredRunway,
    "rangemin": rangeMin,
    "rangemax": rangeMax,
    "city": depAirportCode
}

# get all reachable airports from dep with args
print("getting all possible routes ...")
listFlightsReq, flightsDf = api.getFlights(phpSessidReq, searchParams)
print("Available flights")
availableFlightsDf = flightsDf[["airport","flightUrl","slots","gatesAvailable"]].loc[flightsDf['flightCreated'] == False]
print(availableFlightsDf.to_string(index=False))


# create routes from airport
aircraftType = input("Aircraft type to use: ")
reducedCapacityFlag = input("Allow flights over intended range? (y/n) ")
print("{:20} {:10} {:10} {:10}".format(
        "Destination",
        "First",
        "Business",
        "Economy"
    ))
for idx, flight in availableFlightsDf.iterrows():
    api.createFlight(phpSessidReq, depAirportCode, aircraftType, reducedCapacityFlag, flight)

# TODO when adding flights dont forget to check how many slots are avaiable and order additional or throw error message that the are no gates available
# TODO Add possibility to review made routes and add missing freq

# sandbox
# soup = BeautifulSoup(worldPage.text,'html.parser')
with open("output.html", "w", encoding='utf-8') as file:
    file.write(str(flightListPage))



# TODO

# create api
# chose correct airplane
# auto lease gate / build terminal if possible
# fix ebl bug
# do not do duplicate flights
# split flights on multiple aircrafts (could be done with the dataframe of all aircrafts)

# parse error messages