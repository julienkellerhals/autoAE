import requests
from flask import flash


class AeRequest():
    """AE Request class
    """
    reqCookies = None

    def getRequest(self, url: str, params=None):
        """Get request

        Args:
            url (str): Get request url
            params (str, optional): Request params. Defaults to None.

        Returns:
            r: Request
        """
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
        """Post Request

        Args:
            url (str): post url
            data (dict): post body

        Returns:
            r: request response
        """
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
        """Gets session cookies
        """
        # get page session id
        sessionReqError = True
        while sessionReqError:
            flash("Getting homepage cookies ...")
            _, sessionReqError, _ = self.getRequest(
                url="http://www.airline-empires.com/index.php?/page/home.html"
            )

    def login(self, user: dict) -> bool:
        """Login

        Args:
            user (dict): user data

        Returns:
            bool: login state
        """
        if self.reqCookies is None:
            self.getSessionCookies()

        loginReqError = True
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
        """Gets available worlds

        Returns:
            worldReq: world page
            worldReqError: world request error boolean
        """
        worldReqError = True
        # get worlds
        while worldReqError:
            worldReq, worldReqError, errorCode = self.getRequest(
                url="http://www.airline-empires.com/index.php?app=ae",
            )
            if errorCode == 401:
                break

        return worldReq, worldReqError

    def enterWorld(self, serverInfo: dict):
        enterWorldReqError = True
        while enterWorldReqError:
            # enter world and get php session
            _, enterWorldReqError, _ = self.postRequest(
                url="http://www.airline-empires.com/index.php" \
                    "?app=ae&module=gameworlds&section=enterworld",
                data=serverInfo
            )

    def getMainPage(self):
        mainPageReqError = True
        while mainPageReqError:
            mainPageReq, mainPageReqError, _ = self.getRequest(
                url="http://ae31.airline-empires.com/main.php",
            )
        
        return mainPageReq

    def getAircraft(self, airlineDetailsHref: str):
        getAircraftReqError = True
        while getAircraftReqError:
            getAircraftReq, getAircraftReqError, _ = self.getRequest(
                url=("http://ae31.airline-empires.com/" + airlineDetailsHref),
            )
        
        return getAircraftReq

    def getAircraftDetails(self, aircraftLink: str):
        aircraftDetailReqError = True

        while aircraftDetailReqError:
            getAircraftDetailReq, aircraftDetailReqError, _ = self.getRequest(
                url=("http://ae31.airline-empires.com/" + aircraftLink),
            )

        return getAircraftDetailReq