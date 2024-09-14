import api
import userInput
import AEArgParser
from pony import orm

db = orm.Database()
db.bind(provider="sqlite", filename="autoAE.db", create_db=True)


class Sessions(db.Entity):
    username = orm.Required(str)
    session_id = orm.Required(str)


db.generate_mapping(create_tables=True)
orm.set_sql_debug(True)


@orm.db_session
def main():
    args = AEArgParser.createArgParser()
    username = userInput.setVar(args, "username", "Please enter username: ")

    if len(orm.select(s for s in Sessions if s.username == username)[:]) == 0:
        password = userInput.setVar(args, "password")

        forumSessidReq = api.getPageSession()
        worldReq, airlineDf = api.doLogin(forumSessidReq, username, password)
        phpSessidReq = api.doEnterWorld(args, airlineDf, worldReq)

        s = Sessions(username=username, session_id=dict(
            phpSessidReq.cookies).get("PHPSESSID"))
        orm.commit()

    session_id: str = orm.select(
        s for s in Sessions if s.username == username
    )[:][0].session_id

    aircraftStatsDf = api.getAircraftStats(session_id)
    aircraftList = aircraftStatsDf['aircraft'] \
        .sort_values().astype(str).values.flatten().tolist()

    print("Available aircraft types:")
    print(', '.join(aircraftList))

    aircraftType = userInput.setVar(
        args, "aircraftType", "Aircraft type to use: ")
    flightCountry = userInput.setVar(args, "country", "Flight country: ")
    flightRegion = userInput.setVar(args, "region", "Flight region: ")
    # requiredRunway = userInput.setVar(args, "reqRW", "Minimum runway length: ")
    requiredRunway = aircraftStatsDf['minRunway'].loc[
        aircraftStatsDf['aircraft'] == aircraftType
    ].values[0]

    print("Minimum runway length of {} is {}ft".format(
        aircraftType, requiredRunway)
    )

    rangeMin = userInput.setVar(args, "rgMin", "Flight minimum range: ")
    rangeMax = aircraftStatsDf['range'].loc[
        aircraftStatsDf['aircraft'] == aircraftType
    ].values[0]

    tempRangeMax = userInput.setVar(
        args, "rgMax", "Flight maximum range ({}): ".format(rangeMax))

    if tempRangeMax != '':
        rangeMax = tempRangeMax

    depAirportCode = userInput.setVar(
        args, "depAirportCode", "Departure airport code: ")
    reducedCapacityFlag = userInput.setVar(
        args, "reducedCapacity", "Allow flights over intended range? (y/n) ")
    autoSlots = userInput.setVar(
        args, "autoSlots", "Automatically buy slots? (y/n) ")
    autoTerminal = userInput.setVar(
        args, "autoTerminal", "Automatically build terminal? (y/n) ")
    autoHub = userInput.setVar(
        args, "autoHub", "Automatically create hub? (y/n) ")
    minFreq = userInput.setVar(args, "minFreq", "Aircraft min frequency: ")
    maxFreq = userInput.setVar(args, "maxFreq", "Aircraft max frequency: ")

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

    _, flightsDf = api.getFlights(session_id, searchParams)

    availableFlightsDf = flightsDf[["airport", "flightUrl", "slots",
                                    "gatesAvailable"]].loc[flightsDf['flightCreated'] == False]
    if not availableFlightsDf.empty:
        print("Available flights")
        print(availableFlightsDf.to_string(index=False))

        # Add hub
        if (autoHub == "y"):
            api.addHub(session_id, depAirportCode)

        print("{:20} {:10} {:10} {:10}".format(
            "Destination",
            "First",
            "Business",
            "Economy"
        ))
        for idx, flight in availableFlightsDf.iterrows():
            api.createFlight(
                session_id,
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


if __name__ == "__main__":
    main()
