import argparse
from datetime import datetime
from pathlib import Path
import pandas as pd
from pony.orm import Database, set_sql_debug, Required, Optional, db_session, delete

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
def add_airlines(username: str, airlines: pd.DataFrame):
    delete(a for a in Accounts if a.username == username)
    for _, airline in airlines.iterrows():
        Accounts(
            username=username,
            world=airline["worldName"],
            airline=airline["name"],
            inserted_at=str(datetime.now()),
            updated_at=str(datetime.now())
        )


parser = argparse.ArgumentParser()

parser.add_argument("-u","--username", required=True, help="Username")
parser.add_argument("-p", "--password", required=True, help="Password")

args = parser.parse_args()

forum_session_id_request = api.get_page_session()
world_request, airlines_df = api.do_login(forum_session_id_request, args.username, args.password)
add_airlines(args.username, airlines_df)
