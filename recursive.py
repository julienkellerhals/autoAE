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


# get start route params
recursion = input("Continue previous recursion? (y/n) ")
flightCountry = ''
flightRegion = ''
requiredRunway = input("Minimum runway length: ")
rangeMin = ''
rangeMax = input("Flight maximum range: ")
depAirportCode = input("Departure airport code: ")

# get recursion params
aircraftType = input("Aircraft type to use: ")
reducedCapacityFlag = input("Allow flights over intended range? (y/n) ")
autoSlots = input("Automatically buy slots? (y/n) ")
autoTerminal = input("Automatically build terminal? (y/n) ") 
autoHub = input("Automatically create hub? (y/n) ")
maxFreq = int(input("Aircraft max frequency: "))

if (recursion == 'n'):
    f = open("airportList.csv", "w")
    f.write("airport")
    f.write("\n")
    f.write(depAirportCode)
    f.close()

    f = open("doneAirportList.csv", "w")
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

while len(open("airportList.csv").readlines()) > 1:
    # Read airport list
    doneAirportDf = pd.read_csv("doneAirportList.csv")
    depAirportsDf = pd.read_csv("airportList.csv")

    for _, airport in depAirportsDf.iterrows():
        # replace dep with new airport
        searchParams["city"] = airport['airport']
        # get all reachable airports from dep with args
        print("getting all possible routes ...")
        listFlightsReq, flightsDf = api.getFlights(phpSessidReq, searchParams)

        # Add current destination to done list
        doneAirportSeries = pd.Series(index=["airport"], data=searchParams["city"])
        doneAirportDf = doneAirportDf.append(doneAirportSeries, ignore_index=True)
        doneAirportDf.to_csv("doneAirportList.csv", index=False)

        # Add all new destination to airport list
        depAirportsDf = depAirportsDf.append(flightsDf[["airport"]])
        depAirportsDf = depAirportsDf.drop_duplicates(keep="first")
        depAirportsDf = pd.concat([depAirportsDf, doneAirportDf])
        depAirportsDf = depAirportsDf.drop_duplicates(keep=False)
        depAirportsDf = depAirportsDf[depAirportsDf['airport'] != searchParams["city"]]
        depAirportsDf.to_csv("airportList.csv", index=False)

        print("Available flights")
        availableFlightsDf = flightsDf[["airport","flightUrl","slots","gatesAvailable"]].loc[flightsDf['flightCreated'] == False]
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
                maxFreq,
                flight
            )

print()


# sandbox
