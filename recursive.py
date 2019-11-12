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


# get start route params
recursion = userInput.setVar(args, "recursion", "Continue previous recursion? (y/n) ")
flightCountry = ''
flightRegion = ''
requiredRunway = userInput.setVar(args, "reqRW", "Minimum runway length: ")
rangeMin = ''
rangeMax = userInput.setVar(args, "rgMax", "Flight maximum range: ")
depAirportCode = userInput.setVar(args, "depAirportCode", "Departure airport code: ")

# get recursion params
aircraftType = userInput.setVar(args, "aircraftType", "Aircraft type to use: ")
reducedCapacityFlag = userInput.setVar(args, "reducedCapacity", "Allow flights over intended range? (y/n) ")
autoSlots = userInput.setVar(args, "autoSlots", "Automatically buy slots? (y/n) ")
autoTerminal = userInput.setVar(args, "autoTerminal", "Automatically build terminal? (y/n) ")
autoHub = userInput.setVar(args, "autoHub", "Automatically create hub? (y/n) ")
minFreq = userInput.setVar(args, "minFreq", "Aircraft min frequency: ")
maxFreq = userInput.setVar(args, "maxFreq", "Aircraft max frequency: ")

airportListCsv = "airportList_{}.csv".format(aircraftType)
doneAirportListCsv = "doneAirportList__{}.csv".format(aircraftType)
if (recursion == 'n'):
    f = open(airportListCsv, "w")
    f.write("airport")
    f.write("\n")
    f.write(depAirportCode)
    f.close()

    f = open(doneAirportListCsv, "w")
    f.write("airport")
    f.close()

searchParams = {
    "country": flightCountry,
    "region": flightRegion,
    "runway": requiredRunway,
    "rangemin": rangeMin,
    "rangemax": rangeMax,
    "city": depAirportCode
}

while len(open(airportListCsv).readlines()) > 1:
    # Read airport list
    depAirportsDf = pd.read_csv(airportListCsv)
    doneAirportDf = pd.read_csv(doneAirportListCsv)

    for _, airport in depAirportsDf.iterrows():
        # replace dep with new airport
        searchParams["city"] = airport['airport']
        # get all reachable airports from dep with args
        print("getting all possible routes from {}".format(airport['airport']))
        listFlightsReq, flightsDf = api.getFlights(phpSessidReq, searchParams)

        # Add current destination to done list
        doneAirportSeries = pd.Series(index=["airport"], data=searchParams["city"])
        doneAirportDf = doneAirportDf.append(doneAirportSeries, ignore_index=True)
        doneAirportDf.to_csv(doneAirportListCsv, index=False)

        # Add all new destination to airport list
        depAirportsDf = depAirportsDf.append(flightsDf[["airport"]])
        depAirportsDf = depAirportsDf.drop_duplicates(keep="first")
        depAirportsDf = pd.concat([depAirportsDf, doneAirportDf])
        depAirportsDf = depAirportsDf.drop_duplicates(keep=False)
        depAirportsDf = depAirportsDf[depAirportsDf['airport'] != searchParams["city"]]
        depAirportsDf.to_csv(airportListCsv, index=False)

        availableFlightsDf = flightsDf[["airport","flightUrl","slots","gatesAvailable"]].loc[flightsDf['flightCreated'] == False]
        if not availableFlightsDf.empty:
            print("Available flights")
            print(availableFlightsDf.to_string(index=False))

            # Add hub
            if (autoHub == "y"):
                api.addHub(phpSessidReq, searchParams["city"])

            print("{:20} {:10} {:10} {:10}".format(
                    "Destination",
                    "First",
                    "Business",
                    "Economy"
                ))
            for idx, flight in availableFlightsDf.iterrows():
                api.createFlight(
                    phpSessidReq,
                    searchParams["city"],
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

print()

# sandbox
