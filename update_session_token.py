import argparse
from pathlib import Path
from pony.orm import Database, set_sql_debug, Required, Optional, db_session, select, commit

import api

db = Database()
db.bind(provider="sqlite", filename=str(Path().cwd() / "autoae_dev.db"))

class Accounts(db.Entity):
    username = Required(str)
    world = Required(str)
    airline = Required(str)
    session_id = Optional(str)
    user_id = Optional(int)
    inserted_at = Optional(str)
    updated_at = Optional(str)

db.generate_mapping()
set_sql_debug(True)

@db_session
def add_session_id(username: str, world: str, airline: str, session_id: str):
    w = select(
        a for a in Accounts
        if a.username == username
        and a.world == world
        and a.airline == airline
    )[:][0]
    w.session_id = session_id
    commit()


parser = argparse.ArgumentParser()

parser.add_argument("-u","--username", required=True, help="Username")
parser.add_argument("-p", "--password", required=True, help="Password")
parser.add_argument("-w", "--world", required=True, help="World")
parser.add_argument("-a", "--airline", required=True, help="Airline")

args = parser.parse_args()

forum_session_id_request = api.get_page_session()
world_request, airline_df = api.do_login(forum_session_id_request, args.username, args.password)
php_session_id_request = api.do_enter_world(args.world, args.airline, airline_df, world_request)

add_session_id(args.username, args.world, args.airline, php_session_id_request.cookies.get("PHPSESSID"))
