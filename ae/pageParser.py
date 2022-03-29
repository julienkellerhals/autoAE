from bs4 import BeautifulSoup
import pandas as pd

from ae.aeRequest import getRequest, postRequest

def getSessionCookies():
    # get page session id
    sessionReqError = True
    while sessionReqError:
        print("Getting homepage cookies ...")
        forumSessionIdReq, sessionReqError, _ = getRequest(
            url="http://www.airline-empires.com/index.php?/page/home.html"
        )
    return forumSessionIdReq.cookies

def doLogin(username: str, password: str, sessionCookies):
    loginError = True
    while loginError:
        loginReq = login(sessionCookies, username, password)

        # get world to join
        worldReq, airlineDf, loginError = getWorld(loginReq)
    return worldReq, airlineDf

def login(sessionCookies, username, password):
    loginReqError = True
    user = {
        "auth_key": "880ea6a14ea49e853634fbdc5015a024",
        "ips_username": username,
        "ips_password": password
    }
    # do login
    while loginReqError:
        print("Logging in ...")
        loginReq, loginReqError, _ = postRequest(
            url="http://www.airline-empires.com/index.php?app=core&module=global&section=login&do=process",
            cookies=sessionCookies,
            data=user
        )
    return loginReq

def getWorld(loginReq):
    worldReqError = True
    airlineCols = [
        "worldName",
        "name",
        "idleAircraft",
        "DOP",
        "cash",
        "worldId",
        "userId"
    ]
    airlineDf = pd.DataFrame(columns=airlineCols)
    # get worlds
    while worldReqError:
        worldReq, worldReqError, errorCode = getRequest(
            url="http://www.airline-empires.com/index.php?app=ae",
            cookies=loginReq.cookies
        )
        if (errorCode == 401):
            break
    if not worldReqError:
        worldPage = BeautifulSoup(worldReq.text, 'html.parser')
        htmlWorldList = worldPage.find_all("div","category_block block_wrap")
        for world in htmlWorldList:
            worldName = world.find("h3","maintitle").text
            worldTable = world.find("table")
            airlinesTable = worldTable.find_all("tr", "row1")
            for airlineTable in airlinesTable:
                airlineName = airlineTable.find_all("td")[2].text.strip()
                airlineIdleAircraft = airlineTable.find_all("td")[5].text
                airlineDOP = airlineTable.find_all("td")[7].text
                airlineCash = airlineTable.find_all("td")[8].text
                airlineWorldId = airlineTable.find_all("input")[0].attrs['value'].strip()
                airlineUserId = airlineTable.find_all("input")[1].attrs['value'].strip()
                airline = pd.Series([
                    worldName,
                    airlineName,
                    airlineIdleAircraft,
                    airlineDOP,
                    airlineCash,
                    airlineWorldId,
                    airlineUserId
                ], index=airlineCols)
                airlineDf = airlineDf.append(airline, ignore_index=True)
        print(airlineDf.to_string(columns=[
            "worldName",
            "name",
            "idleAircraft",
            "DOP",
            "cash"
        ], index=False))
    return worldReq, airlineDf, worldReqError