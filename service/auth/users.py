import json
import random
from pathlib import Path

from service.auth.user import User


class Users():
    path: Path = Path(Path.cwd(), "service/auth/auth.json")
    userList: dict = {}

    def __init__(self) -> None:
        if self.path.is_file():
            with open(self.path) as f:
                self.userList = json.load(f)
        else:
            self.path.touch()
            self.writeJson()

    def writeJson(self) -> None:
        with open(self.path, "w") as f:
                json.dump(self.userList, f)

    def get(self, userId: str) -> User:
        if not userId in self.userList.keys():
            return None
        user: dict = self.userList[userId]
        return User(
            user["is_authenticated"],
            user["is_active"],
            user["is_anonymous"],
            userId,
            user["username"]
        )

    def getPasswordHash(self, username: str) -> str:
        pwHash = None
        queryRes = [self.userList[u] for u in self.userList if self.userList[u]["username"] == username]
        if len(queryRes) > 0:
            pwHash = queryRes[0]["password"]
        return pwHash

    def getMemberId(self, username: str) -> str:
        userId: str = None
        queryRes = [u for u in self.userList if self.userList[u]["username"] == username]
        if len(queryRes) > 0:
            userId = queryRes[0]
        return userId

    def createUser(self, username: str, pwHash: str) -> None:
        userId = random.randint(0, 100000)
        user: dict = {}
        user["is_authenticated"] = False
        user["is_active"] = True
        user["is_anonymous"] = False
        user["username"] = username
        user["password"] = pwHash
        self.userList[userId] = user

        self.writeJson()

    def setAuth(self, userId: str, authStatus: bool) -> None:
        user: dict = self.userList[userId]
        user["is_authenticated"] = authStatus

        self.writeJson()
