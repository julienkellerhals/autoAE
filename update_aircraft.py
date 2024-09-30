import argparse

from api import get_aircraft_stats
from models.accounts import get_account_by_id
from models.aircraft import add_aircraft

parser = argparse.ArgumentParser()

parser.add_argument("--account_id", required=True, help="Account ID")
parser.add_argument("--user_id", required=True, help="User id")

args = parser.parse_args()


def main() -> None:
    account = get_account_by_id(args.account_id)

    aircraft_stats_df = get_aircraft_stats(account.session_id)
    add_aircraft(args.account_id, aircraft_stats_df, int(args.user_id))


if __name__ == "__main__":
    main()
