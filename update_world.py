import argparse

import api
from db import add_airlines

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--username", required=True, help="Username")
parser.add_argument("-p", "--password", required=True, help="Password")

args = parser.parse_args()


def main() -> None:
    forum_session_id_request = api.get_page_session()
    _, airlines_df = api.do_login(
        forum_session_id_request, args.username, args.password
    )
    add_airlines(args.username, airlines_df)


if __name__ == "__main__":
    main()
