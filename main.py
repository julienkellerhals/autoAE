import api
import userInput
import AEArgParser
from pony.orm import Database, Required, db_session, select, commit

from api import get_request

db = Database()
db.bind(provider="sqlite", filename="autoAE.db", create_db=True)


class Sessions(db.Entity):
    username = Required(str)
    session_id = Required(str)


db.generate_mapping(create_tables=True)
# orm.set_sql_debug(True)


def get_session_id(args, username: str):
    password = userInput.setVar(args, "password")

    forumSessidReq = api.get_page_session()
    worldReq, airlineDf = api.doLogin(forumSessidReq, username, password)
    phpSessidReq = api.doEnterWorld(args, airlineDf, worldReq)

    s = Sessions(username=username, session_id=dict(
        phpSessidReq.cookies).get("PHPSESSID"))
    commit()


@db_session
def main():
    args = AEArgParser.createArgParser()
    username = userInput.setVar(args, "username", "Please enter username: ")

    if len(select(s for s in Sessions if s.username == username)[:]) == 0:
        get_session_id(args, username)

    session_id: str = select(
        s for s in Sessions if s.username == username
    )[:][0].session_id

    mainPageReq, _, _ = get_request(
        url="http://ae31.airline-empires.com/main.php",
        cookies={"PHPSESSID": session_id}
    )

    if mainPageReq.text == "<script type='text/javascript'>window.location = 'http://www.airline-empires.com/index.php?app=ae';</script>":
        get_session_id(args, username)

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
