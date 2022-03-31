from datetime import datetime
import pandas as pd

from ae.aeRequest import AeRequest
from ae.pageParser import PageParser

class Datastore():
    req: AeRequest = None
    parser: PageParser = None
    datastore: dict = {}

    def __init__(self) -> None:
        self.req = AeRequest()
        self.parser = PageParser()
        self.datastore["airlines"] = {}
        self.datastore["airlines"]["airlineCols"] = [
            "worldName",
            "name",
            "idleAircraft",
            "DOP",
            "cash",
            "worldId",
            "userId"
        ]
        self.datastore["airlines"]["airlineDf"] = pd.DataFrame(
            columns=self.datastore["airlines"]["airlineCols"]
        )

    def login(self, username: str, password: str):
        self.datastore["login"] = {}
        self.datastore["login"]["status"] = self.req.login(username, password)
        self.datastore["login"]["time"] = datetime.now()

    def getWorld(self):
        worldReq, worldReqError = self.req.getWorld()
        airlineDf = self.datastore["airlines"]["airlineDf"]
        airlineCols = self.datastore["airlines"]["airlineCols"]

        if not worldReqError:
            airlineDf = self.parser.getWorld(
                worldReq.text,
                airlineDf,
                airlineCols
            )
            self.datastore["airlines"]["airlineDf"] = airlineDf

    def enterWorld(self, worldId: str, userId: str):
        serverInfo = {
            "world": worldId,
            "userid": userId
        }
        self.req.enterWorld(serverInfo)
