import argparse

from api import get_page_session, do_login
from models.accounts import update_airlines

parser = argparse.ArgumentParser()

parser.add_argument("--username", required=True, help="Username")
parser.add_argument("--password", required=True, help="Password")
parser.add_argument("--user_id", required=True, help="User id")

args = parser.parse_args()


def main() -> None:
    forum_session_id_request = get_page_session()
    _, airlines_df = do_login(forum_session_id_request, args.username, args.password)
    update_airlines(args.username, int(args.user_id), airlines_df)


if __name__ == "__main__":
    main()
