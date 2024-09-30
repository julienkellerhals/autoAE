import sys
from typing import Optional
from datetime import datetime

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column

from models.db import Base
from models.db import ENGINE


class Accounts(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    world: Mapped[str]
    airline: Mapped[str]
    session_id: Mapped[Optional[str]]
    user_id: Mapped[Optional[str]]
    inserted_at: Mapped[str]
    updated_at: Mapped[str]


def get_account_by_username_world_airline(
    username: str, world: str, airline: str, session: Session | None = None
) -> Accounts:
    if session is None:
        session = Session(ENGINE)

    stmt = (
        select(Accounts)
        .where(Accounts.username == username)
        .where(Accounts.world == world)
        .where(Accounts.airline == airline)
    )

    account = session.scalar(stmt)

    if account is None:
        sys.exit()

    return account


def get_account_by_id(_id: int) -> Accounts:
    session = Session(ENGINE)

    stmt = select(Accounts).where(Accounts.id == _id)

    account = session.scalar(stmt)

    if account is None:
        sys.exit()

    return account


def add_airlines(username: str, airlines: pd.DataFrame) -> None:
    session = Session(ENGINE)

    for _, airline in airlines.iterrows():
        account = Accounts(
            username=username,
            world=airline["worldName"],
            airline=airline["name"],
            inserted_at=str(datetime.now()),
            updated_at=str(datetime.now()),
        )
        session.add(account)
        session.commit()


def add_session_id(username: str, world: str, airline: str, session_id: str) -> None:
    session = Session(ENGINE)

    account = get_account_by_username_world_airline(username, world, airline, session)

    if account is None:
        sys.exit()

    account.session_id = session_id
    session.commit()
