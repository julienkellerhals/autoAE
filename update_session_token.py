import argparse

import api
from models.accounts import add_session_id

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--username", required=True, help="Username")
parser.add_argument("-p", "--password", required=True, help="Password")
parser.add_argument("-w", "--world", required=True, help="World")
parser.add_argument("-a", "--airline", required=True, help="Airline")
parser.add_argument("--user_id", required=True, help="User id")

args = parser.parse_args()


def main() -> None:
    forum_session_id_request = api.get_page_session()
    world_request, airline_df = api.do_login(
        forum_session_id_request, args.username, args.password
    )
    php_session_id_request = api.do_enter_world(
        args.world, args.airline, airline_df, world_request
    )

    add_session_id(
        user_id=args.user_id,
        username=args.username,
        world=args.world,
        airline=args.airline,
        session_id=php_session_id_request.cookies.get("PHPSESSID"),
    )


if __name__ == "__main__":
    main()
