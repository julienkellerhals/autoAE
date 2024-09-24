import argparse

import api
from db import get_session_id_by_id, add_aircraft

parser = argparse.ArgumentParser()

parser.add_argument("--id", required=True, help="Account ID")

args = parser.parse_args()


def main() -> None:
    session_id = get_session_id_by_id(args.id)

    aircraft_stats_df = api.get_aircraft_stats(session_id)
    add_aircraft(args.id, aircraft_stats_df)


if __name__ == "__main__":
    main()
