import requests
from flask import flash


class AeRequest():
    reqCookies = None

    def getRequest(self, url: str, params=None):
        r = None
        reqError = True
        errorCode = None
        try:
            r = requests.get(
                url=url,
                cookies=self.reqCookies,
                params=params,
                timeout=210
            )
            r.raise_for_status()
            reqError = False
            self.reqCookies = r.cookies
        except requests.exceptions.Timeout as e:
            print("request timed-out")
            print(e)
        except requests.exceptions.ConnectionError as e:
            print("connection error")
            print(e)
        except requests.exceptions.HTTPError as e:
            errorCode = r.status_code
            print(e)
        except requests.exceptions.ChunkedEncodingError as e:
            print("connection error")
            print(e)

        return r, reqError, errorCode

    def postRequest(self, url: str, data: dict):
        r = None
        reqError = True
        errorCode = None
        try:
            r = requests.post(
                url,
                cookies=self.reqCookies,
                data=data,
                timeout=210
            )
            r.raise_for_status()
            reqError = False
            self.reqCookies = r.cookies
        except requests.exceptions.Timeout as e:
            print("request timed-out")
            print(e)
        except requests.exceptions.ConnectionError as e:
            print("connection error")
            print(e)
        except requests.exceptions.HTTPError as e:
            errorCode = r.status_code
            print(e)
        except requests.exceptions.ChunkedEncodingError as e:
            print("connection error")
            print(e)

        return r, reqError, errorCode

    def getSessionCookies(self):
        # get page session id
        sessionReqError = True
        while sessionReqError:
            flash("Getting homepage cookies ...")
            _, sessionReqError, _ = self.getRequest(
                url="http://www.airline-empires.com/index.php?/page/home.html"
            )

    def login(self, username: str, password: str) -> bool:
        if self.reqCookies is None:
            self.getSessionCookies()

        loginReqError = True
        user = {
            "auth_key": "880ea6a14ea49e853634fbdc5015a024",
            "ips_username": username,
            "ips_password": password
        }
        # do login
        for _ in range(5):
            print("Logging in ...")
            _, loginReqError, _ = self.postRequest(
                url="http://www.airline-empires.com/index.php" \
                    "?app=core&module=global&section=login&do=process",
                data=user
            )
            if not loginReqError:
                return True

        flash("Error while login in", "error")
        return False

    def getWorld(self):
        worldReqError = True
        # get worlds
        while worldReqError:
            worldReq, worldReqError, errorCode = self.getRequest(
                url="http://www.airline-empires.com/index.php?app=ae",
            )
            if errorCode == 401:
                break

        return worldReq, worldReqError
