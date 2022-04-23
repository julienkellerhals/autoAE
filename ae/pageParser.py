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
        aircraftHrefList = aircraftListPage.find_all(
            "a",
            href = re.compile(r'acdata.php\?aircraft*')
        )
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

    def getFlightList(self, page: str, flightsCols: list, flightsDf: pd.DataFrame):
        slotsRegex = r"\((\d*).*\)"
        flightListPage = BeautifulSoup(page, 'html.parser')
        flightListTable = flightListPage.find_all("form")[1]
        flightList = flightListTable.find_all("tr")[1:]
        for flightRow in flightList:
            airport = flightRow.find_all("td")[0].text
            try:
                flightUrl = flightRow.find_all("td")[5].find("a").attrs['href']
            except AttributeError as e:
                # print("Flight from {} to {} cannot be researched".format(searchParams["city"], airport))
                print(e)
            else:
                if flightRow.find_all("td")[5].find("div") is None:
                    flightCreated = False
                else:
                    flightCreated  = True
                try:
                    slots = re.search(slotsRegex, flightRow.find_all("td")[6].text).group(1)
                except AttributeError:
                    slots = None
                if flightRow.find_all("td")[10].find("input") is None:
                    gatesAvailable = False
                else:
                    gatesAvailable = True
                flight = pd.Series([
                    airport,
                    flightUrl,
                    flightCreated,
                    slots,
                    gatesAvailable
                ], index=flightsCols)
                flightsDf = flightsDf.append(flight, ignore_index=True)
        return flightsDf

    def getFlightDemand(self, page: str):
        routeDetailsPage = BeautifulSoup(page, 'html.parser')
        highChartsScript = str(routeDetailsPage.findAll('script')[10])
        rawData = re.findall(r"data: \[\d*,\d*,\d*\]", highChartsScript)[0]
        flightDemand = [int(x) for x in re.findall(r"\d*,\d*,\d*", rawData)[0].split(',')]
        print()
        print("{:10} {:10} {:10}".format(
            flightDemand[0],
            flightDemand[1],
            flightDemand[2])
        )
        return flightDemand

    def getAvailableAircrafts(
        self,
        page: str,
        availableAircraftsCols: list,
    ):
        availableAircraftsDf = pd.DataFrame(columns=availableAircraftsCols)
        availableAircraftsPage = BeautifulSoup(page, 'html.parser')
        newFlightsPage = availableAircraftsPage.find("div", {"id": "newflights"})
        availableAircraftsTable = newFlightsPage.find(
            "td",
            text="Type"
        ).parent.parent.find_all("tr", recursive=False)[1:]

        for availableAircraftRow in availableAircraftsTable:
            aircraftData = availableAircraftRow.find_all('td', recursive=False)

            if (
                aircraftData[0].text ==
                "You do not have any aircraft available to serve this route."
            ):
                print(
                    "You do not have any aircraft available to serve this route."
                    "(May also be a bug in AE code)"
                )
            else:
                frequency = aircraftData[0].find_all('option')[-1:][0].text

            aircraftId = aircraftData[1].text
            aircraftType = aircraftData[2].text

            try:
                seatF = int(aircraftData[3].find_all('td')[-3:-2][0].text.strip(' F'))
            except IndexError:
                seatF = 0

            try:
                seatC = int(aircraftData[3].find_all('td')[-2:-1][0].text.strip(' C'))
            except IndexError:
                seatC = 0

            try:
                seatY = int(aircraftData[3].find_all('td')[-1:][0].text.strip(' Y'))
            except IndexError:
                seatY = 0

            if aircraftData[4].find_all('span') == []:
                reducedCapacity = False
            else:
                reducedCapacity = True

            hours = aircraftData[5].text

            aircraft = pd.Series([
                frequency,
                aircraftId,
                aircraftType,
                seatF,
                seatC,
                seatY,
                reducedCapacity,
                hours
            ], index=availableAircraftsCols)
            availableAircraftsDf = availableAircraftsDf.append(aircraft, ignore_index=True)

        return availableAircraftsDf

    def getFlightInfo(self, page: str):
        availableAircraftsPage = BeautifulSoup(page, 'html.parser')
        newFlightsPage = availableAircraftsPage.find("div", {"id": "newflights"})

        # get prices and ifs
        flightInfo = newFlightsPage.find('div', 'prices')
        if flightInfo is not None:
            flightInfo = flightInfo.contents[0]
            flightInfoPrices = []
            try:
                for allFlightPrices in flightInfo.contents[3].findAll('input'):
                    flightInfoPrices.append(allFlightPrices.attrs['value'])
            except:
                pass

            flightInfoIFS = []
            try:
                for allFlightIFS in flightInfo.contents[4].findAll('option'):
                    try:
                        allFlightIFS.attrs['selected']
                        flightInfoIFS.append(allFlightIFS.attrs['value'])
                    except KeyError:
                        pass
            except:
                for allFlightIFS in flightInfo.find_all("a"):
                    flightInfoIFS.append(allFlightIFS.attrs['href'].split('id=')[-1:][0])

        return flightInfo, flightInfoPrices, flightInfoIFS

    def getGateUtilization(self, page: str):
        gateUtilizationPage = BeautifulSoup(page, 'lxml')
        gateUtilizationTable = gateUtilizationPage.find(id='airline_airport_list')
        gateTableHeaders = self.trToList(gateUtilizationTable.find_all('tr')[0].findAll('td'))
        gateTableRowList = []
        for tr in gateUtilizationTable.find_all('tr')[1:]:
            gateTableRow = self.trToList(tr)
            gateTableRowList.append(dict(zip(gateTableHeaders, gateTableRow)))
        gateUtilizationDf = pd.DataFrame(gateTableRowList)
        gateUtilizationDf = gateUtilizationDf.astype(
            dict(zip(gateTableHeaders, ['str','str','int','str']))
        )

        return gateUtilizationDf

    def getTerminal(self, page: str, airport: str):
        getTerminalPage = BeautifulSoup(page, 'html.parser')
        # Not safe, redo
        try:
            gateAmount = int(getTerminalPage.find(text=airport).next.next.next) + 5
        except AttributeError:
            gateAmount = 5

        return gateAmount
