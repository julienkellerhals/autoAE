import re
import pandas as pd
from bs4 import BeautifulSoup

class PageParser():

    def trToList(self, tr):
        rowList = []
        for td in tr:
            if td != '\n':
                rowList.append(td.text)
        return rowList

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
                link = f"<a href='/ae/airlines/join?world={worldId}&amp;player={userId}'>{name}</a>"
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

    def getAirlineDetails(self, page: str):
        mainPage = BeautifulSoup(page, 'lxml')
        return mainPage.find('a', text="Airline Details").attrs['href']

    def getAircraftList(self, page: str):
        aircraftListPage = BeautifulSoup(page, 'lxml')
        aircraftHrefList = aircraftListPage.find_all("a", href = re.compile(r'acdata.php\?aircraft*'))
        return list(dict.fromkeys(aircraftHrefList))

    def getAircraftDetails(self, page: str, aircraftStatsCols: list, aircraftStatsDf: pd.DataFrame):
        aircraftDetailPage = BeautifulSoup(page, 'lxml')
        aircraftName = aircraftDetailPage.find_all(
            "div",
            class_="pagetitle"
        )[0].text.replace(" Aircraft Information", '')
        link = f"<a href='/ae/flight/use?aircraft={aircraftName}'>{aircraftName}</a>"

        engineInfoTable = aircraftDetailPage.find_all("table")[-1]

        maxRangeEngineSeries = pd.Series(['',0,0], index=aircraftStatsCols)
        for tr in engineInfoTable.find_all('tr')[1:]:
            engineTableRow = self.trToList(tr)
            engineRange = int(re.sub(r' mi.*', '', engineTableRow[7]).replace(',',''))
            engineMinRunway = int(engineTableRow[9].replace(',',''))

            aircraftStats = pd.Series([
                link,
                engineRange,
                engineMinRunway
            ], index=aircraftStatsCols)

            if maxRangeEngineSeries['range'] < aircraftStats['range']:
                maxRangeEngineSeries = aircraftStats
        return aircraftStatsDf.append(maxRangeEngineSeries, ignore_index=True)
