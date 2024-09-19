import api
import AEArgParser

args = AEArgParser.createArgParser()
forumSessidReq = api.get_page_session()
worldReq, airlineDf = api.doLogin(args, forumSessidReq)
phpSessidReq = api.doEnterWorld(args, airlineDf, worldReq)

while True:
    routesDf = api.getRoutes(phpSessidReq, 1)

    action = input("Action to execute on routes? ")
    if (action == 'close'):
        api.closeRoutes(phpSessidReq, routesDf)
print()
