import api
import userInput
import AEArgParser
from bs4 import BeautifulSoup
from pony.orm import Database, Required, PrimaryKey, db_session, select, commit

from api import getRequest, postRequest

db = Database()
db.bind(provider="sqlite", filename="autoAE.db", create_db=True)


class Sessions(db.Entity):
    username = Required(str)
    session_id = Required(str)


class UsedMarketAircraft(db.Entity):
    aircraft_id = Required(int)
    name = Required(str)
    count = Required(int)


db.generate_mapping(create_tables=True)
# orm.set_sql_debug(True)


def get_session_id(args, username: str):
    password = userInput.setVar(args, "password")

    forumSessidReq = api.getPageSession()
    worldReq, airlineDf = api.doLogin(forumSessidReq, username, password)
    phpSessidReq = api.doEnterWorld(args, airlineDf, worldReq)

    s = Sessions(
        username=username, session_id=dict(phpSessidReq.cookies).get("PHPSESSID")
    )
    commit()


@db_session
def main():
    args = AEArgParser.createArgParser()
    username = userInput.setVar(args, "username", "Please enter username: ")

    if len(select(s for s in Sessions if s.username == username)[:]) == 0:
        get_session_id(args, username)

    session_id: str = select(s for s in Sessions if s.username == username)[:][
        0
    ].session_id

    mainPageReq, _, _ = getRequest(
        url="http://ae31.airline-empires.com/main.php",
        cookies={"PHPSESSID": session_id},
    )

    if (
        mainPageReq.text
        == "<script type='text/javascript'>window.location = 'http://www.airline-empires.com/index.php?app=ae';</script>"
    ):
        get_session_id(args, username)

    market_buy_page_req, _, _ = getRequest(
        url="https://ae31.airline-empires.com/aircraft_market_buy.php",
        cookies={"PHPSESSID": session_id},
    )
    market_buy_page = BeautifulSoup(market_buy_page_req.text, "lxml")
    all_types: list = market_buy_page.find_all("option")

    filtered_types: list = [t for t in all_types if t.attrs.get("value", "").isdigit()]

    for aircraft_type in filtered_types:
        _ = UsedMarketAircraft(
            aircraft_id=aircraft_type.attrs.get("value"),
            name=aircraft_type.text.split("(")[0].strip(),
            count=int(aircraft_type.text.split("(")[1].strip(")")),
        )
        commit()

    maker_market_buy_page_req, _, _ = getRequest(
        url="https://ae31.airline-empires.com/aircraft_market_buy.php?maker=26&order=manufacturer%2C+type&sort=ASC",
        cookies={"PHPSESSID": session_id},
        params={"maker": 182, "next": -1},
    )
    maker_market_buy_page = BeautifulSoup(maker_market_buy_page_req.text, "lxml")
    table_input: list = maker_market_buy_page.find("form", method="post").find_all(
        "input"
    )
    aircraft_ids: list = [
        i.attrs.get("value")
        for i in table_input
        if i.attrs.get("name") == "aircraftid[]"
    ]

    for aircraft_id in aircraft_ids:
        _req, _, _ = postRequest(
            url="https://ae31.airline-empires.com/aircraft_lease_confirm.php",
            cookies={"PHPSESSID": session_id},
            data={"mode": "lease", "aircraftid": aircraft_id, "length": 10},
        )

        print("end")


if __name__ == "__main__":
    main()
