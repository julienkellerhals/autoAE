import api
from bs4 import BeautifulSoup
from getpass import getpass
import pandas as pd

loginError = True
while loginError:
    # get password and login
    username = input("Please enter username: ")
    password = getpass()
    loginReq = api.login(username, password)

    # get world to join
    worldReq, airlineDf, loginError = api.getWorld(loginReq)

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
autoSlots = input("Automatically buy slots? (y/n) ")
maxFreq = int(input("Aircraft max frequency: "))
print("{:20} {:10} {:10} {:10}".format(
        "Destination",
        "First",
        "Business",
        "Economy"
    ))
for idx, flight in availableFlightsDf.iterrows():
    api.createFlight(
        phpSessidReq,
        depAirportCode,
        aircraftType,
        reducedCapacityFlag,
        autoSlots,
        maxFreq,
        flight
    )


# sandbox
# soup = BeautifulSoup(worldPage.text,'html.parser')
# with open("output.html", "w", encoding='utf-8') as file:
#     file.write(str(flightListPage))



# TODO
# TODO when adding flights dont forget to check how many slots are avaiable and order additional or throw error message that the are no gates available
# TODO Add possibility to review made routes and add missing freq
# TODO Review existing flights if it achieves demand
# TODO Fix no available aircraft is wrong
# TODO Add dataviz for freq by class by plane, to findo ut which plane size is required

# TODO Important
# Request timeout and retry
# recursion
# arg parser
# TODO Limit amount of new aircrafts to use!
# minimum frequency
# List of airports to do (write to csv from route list)

# parse error messages