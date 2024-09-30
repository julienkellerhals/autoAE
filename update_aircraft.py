import argparse

from api import get_aircraft_stats
from models.accounts import get_account_by_id
from models.aircraft import add_aircraft

parser = argparse.ArgumentParser()

parser.add_argument("--account_id", required=True, help="Account ID")

args = parser.parse_args()


def main() -> None:
    account = get_account_by_id(args.account_id)

    aircraft_stats_df = get_aircraft_stats(account.session_id)
    add_aircraft(args.account_id, aircraft_stats_df)


if __name__ == "__main__":
    main()
