import pandas as pd
from bs4 import BeautifulSoup

class PageParser():

    def getWorld(self, page: str, airlineDf: pd.DataFrame, airlineCols: dict):
        worldPage = BeautifulSoup(page, 'html.parser')
        htmlWorldList = worldPage.find_all("div","category_block block_wrap")
        for world in htmlWorldList:
            worldName = world.find("h3","maintitle").text
            worldTable = world.find("table")
            airlinesTable = worldTable.find_all("tr", "row1")
            for airlineTable in airlinesTable:
                name = airlineTable.find_all("td")[2].text.strip()
                idleAircraft = airlineTable.find_all("td")[5].text
                dop = airlineTable.find_all("td")[7].text
                cash = airlineTable.find_all("td")[8].text
                worldId = airlineTable.find_all("input")[0].attrs['value'].strip()
                userId = airlineTable.find_all("input")[1].attrs['value'].strip()
                link = f"<a href='/ae/world/join?world={worldId}&amp;player={userId}'>{name}</a>"
                airline = pd.Series([
                    worldName,
                    link,
                    idleAircraft,
                    dop,
                    cash,
                    worldId,
                    userId
                ], index=airlineCols)
                airlineDf = airlineDf.append(airline, ignore_index=True)
        return airlineDf
