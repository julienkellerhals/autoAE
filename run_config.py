import argparse
from pony.orm import db_session

import api
from db import get_session_id_by_id, get_configuration_by_id

parser = argparse.ArgumentParser()

parser.add_argument("--account_id", required=True, help="Account ID")
parser.add_argument("--configuration_id", required=True, help="Configuration ID")

args = parser.parse_args()


@db_session
def main() -> None:
    session_id = get_session_id_by_id(args.account_id)
    configuration = get_configuration_by_id(args.configuration_id)

    search_params = {
        "country": configuration["country"],
        "region": configuration["region"],
        "runway": configuration["min_runway"],
        "rangemin": configuration["min_range"],
        "rangemax": configuration["max_range"],
        "city": configuration["departure_airport_code"],
    }

    search_params = {k: ("" if v is None else v) for k, v in search_params.items()}

    _, flights_df = api.get_flights(session_id, search_params)

    available_flights_df = flights_df.loc[flights_df["flightCreated"] == False]  # noqa: E712

    if not available_flights_df.empty:
        print("Available flights")
        print(available_flights_df.to_string(index=False))

        # Add hub
        if configuration["auto_hub"] == "y":
            api.add_hub(session_id, configuration["departure_airport_code"])

        for _, flight in available_flights_df.iterrows():
            api.create_flight(
                session_id=session_id,
                departure_airport_code=configuration["departure_airport_code"],
                aircraft=configuration["aircraft"],
                reduced_capacity_flag=False,
                auto_slot=configuration["auto_slot"],
                auto_terminal=configuration["auto_terminal"],
                min_frequency=configuration["min_frequency"],
                max_frequency=configuration["max_frequency"],
                flight=flight,
            )
    else:
        print("No new flights available.")


if __name__ == "__main__":
    main()
