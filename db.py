import sys
from pathlib import Path
from datetime import datetime

import pandas as pd

from pony.orm import (
    Database,
    Required,
    db_session,
    set_sql_debug,
    Optional,
    select,
    commit,
    delete,
)


DB_FILE = "autoae_dev.db"

db = Database()
db.bind(provider="sqlite", filename=str(Path().cwd() / DB_FILE))


class Accounts(db.Entity):
    username = Required(str)
    world = Required(str)
    airline = Required(str)
    session_id = Optional(str)
    user_id = Optional(int)
    inserted_at = Required(str)
    updated_at = Required(str)


@db_session
def get_session_id_by_username(username: str, world: str, airline: str) -> str:
    a: Accounts = select(
        a
        for a in Accounts  # type: ignore
        if a.username == username and a.world == world and a.airline == airline
    ).first()

    return a.session_id  # type: ignore


@db_session
def get_session_id_by_id(_id: int) -> str:
    account: Accounts = Accounts.get(id=_id)  # type: ignore

    if account is None:
        sys.exit()

    return account.session_id  # type: ignore


@db_session
def add_session_id(username: str, world: str, airline: str, session_id: str) -> None:
    a: Accounts | None = select(
        a
        for a in Accounts  # type: ignore
        if a.username == username and a.world == world and a.airline == airline
    ).first()

    if a is not None:
        a.session_id = session_id
        commit()


@db_session
def add_airlines(username: str, airlines: pd.DataFrame) -> None:
    delete(a for a in Accounts if a.username == username)  # type: ignore

    for _, airline in airlines.iterrows():
        Accounts(
            username=username,
            world=airline["worldName"],
            airline=airline["name"],
            inserted_at=str(datetime.now()),
            updated_at=str(datetime.now()),
        )


class Aircraft(db.Entity):
    aircraft = Required(str)
    range = Required(int)
    min_runway = Required(int)
    account_id = Required(int)
    user_id = Optional(int)
    inserted_at = Optional(str)
    updated_at = Optional(str)


@db_session
def add_aircraft(account_id: int, aircraft_stats: pd.DataFrame):
    for _, aircraft in aircraft_stats.iterrows():
        Aircraft(
            aircraft=aircraft["aircraft"],
            range=aircraft["range"],
            min_runway=aircraft["min_runway"],
            account_id=account_id,
            # TODO add user id
            inserted_at=str(datetime.now()),
            updated_at=str(datetime.now()),
        )


db.generate_mapping()
set_sql_debug(True)
