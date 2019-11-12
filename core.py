import AEArgParser
import userInput
import api
from bs4 import BeautifulSoup
import pandas as pd

args = AEArgParser.createArgParser()

loginError = True
while loginError:
    # get password and login
    username = userInput.setVar(args, "username", "Please enter username: ")
    password = userInput.setVar(args, "password")
    loginReq = api.login(username, password)

    # get world to join
    worldReq, airlineDf, loginError = api.getWorld(loginReq)

tryServer = True
while tryServer:
    airlineName = userInput.setVar(args, "airline", "Please enter one of above mentioned airline names: ")
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
flightCountry = userInput.setVar(args, "country", "Flight country: ")
flightRegion = userInput.setVar(args, "region", "Flight region: ")
requiredRunway = userInput.setVar(args, "reqRW", "Minimum runway length: ")
rangeMin = userInput.setVar(args, "rgMin", "Flight minimum range: ")
rangeMax = userInput.setVar(args, "rgMax", "Flight maximum range: ")
depAirportCode = userInput.setVar(args, "depAirportCode", "Departure airport code: ")

searchParams = {
    "country": flightCountry,
    "region": flightRegion,
    "runway": requiredRunway,
    "rangemin": rangeMin,
    "rangemax": rangeMax,
    "city": depAirportCode
}

# get all reachable airports from dep with args
print("getting all possible routes from {}".format(depAirportCode))
listFlightsReq, flightsDf = api.getFlights(phpSessidReq, searchParams)
availableFlightsDf = flightsDf[["airport","flightUrl","slots","gatesAvailable"]].loc[flightsDf['flightCreated'] == False]
if not availableFlightsDf.empty:
    print("Available flights")
    print(availableFlightsDf.to_string(index=False))

    # create routes from airport
    aircraftType = userInput.setVar(args, "aircraftType", "Aircraft type to use: ")
    reducedCapacityFlag = userInput.setVar(args, "reducedCapacity", "Allow flights over intended range? (y/n) ")
    autoSlots = userInput.setVar(args, "autoSlots", "Automatically buy slots? (y/n) ")
    autoTerminal = userInput.setVar(args, "autoTerminal", "Automatically build terminal? (y/n) ")
    autoHub = userInput.setVar(args, "autoHub", "Automatically create hub? (y/n) ")
    minFreq = userInput.setVar(args, "minFreq", "Aircraft min frequency: ")
    maxFreq = userInput.setVar(args, "maxFreq", "Aircraft max frequency: ")

    # Add hub
    if (autoHub == "y" or autoHub == True):
        api.addHub(phpSessidReq, depAirportCode)

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
            autoTerminal,
            minFreq,
            maxFreq,
            flight
        )
else:
    print("No new flights available.")



# sandbox
# soup = BeautifulSoup(worldPage.text,'html.parser')
# with open("output.html", "w", encoding='utf-8') as file:
#     file.write(str(routeDetailsPage))



# TODO
# TODO Add possibility to review made routes and add missing freq
# TODO Review existing flights if it achieves demand
# TODO Fix no available aircraft is wrong
# TODO Add dataviz for freq by class by plane, to findo ut which plane size is required
# TODO Subprocess controller
# TODO Create auto rec with json

# TODO Important
# arg parser
# TODO Limit amount of new aircrafts to use!
# TODO aircraft list

# parse error messages