import pandas as pd

airlineCols = [
    "worldName",
    "name",
    "idleAircraft",
    "DOP",
    "cash",
    "worldId",
    "userId"
]

aircraftStatsCols = [
    "aircraft",
    "range",
    "minRunway"
]

datastoreBase = {
    "login": {},
    "airlines": {
        "airlineCols": airlineCols,
        "airlineDf": pd.DataFrame(columns=airlineCols)
    },
    "aircraftStats": {
        "aircraftStatsCols": aircraftStatsCols,
        "aircraftStatsDf": pd.DataFrame(columns=aircraftStatsCols)
    }
}
