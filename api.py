import requests
from bs4 import BeautifulSoup
import re
import math
import cred
import pandas as pd

# get page session id
print("Getting homepage cookies ...")
forumSessidReq = requests.get("http://www.airline-empires.com/index.php?/page/home.html")

def login(username, password):
    cred.user['ips_username'] = username
    cred.user['ips_password'] = password
    # do login
    print("Logging in ...")
    loginReq = requests.post(
        "http://www.airline-empires.com/index.php?app=core&module=global&section=login&do=process",
        cookies=forumSessidReq.cookies,
        data=cred.user
    )
    print("logged in with user: {}".format(cred.user['ips_username']))
    return loginReq

def getWorld(loginReq):
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
    print("getting all worlds ...")
    worldReq = requests.get(
        "http://www.airline-empires.com/index.php?app=ae",
        cookies=loginReq.cookies,
    )
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
    return worldReq, airlineDf

def enterWorld(worldReq, gameServer):
    # enter world and get php session
    phpSessidReq = requests.post(
        "http://www.airline-empires.com/index.php?app=ae&module=gameworlds&section=enterworld",
        cookies=worldReq.cookies,
        data=gameServer
    )
    return phpSessidReq
