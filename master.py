import api
import AEArgParser
import pickle
import subprocess
import json

def getCmd(cmd, config):
    for configKey in config.keys():
        cmd += '--' + configKey
        if ' ' in config[configKey]:
            cmd += ' "' + config[configKey] + '" '
        else:
            cmd += " " + config[configKey] + " "
    return cmd

def createSubProc(cmd):
    if (consoleType == 'y'):
        proc = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        proc = subprocess.Popen(cmd, shell=True)
    print(proc.pid)
    print(proc.stdout)
    print(proc.stderr)
    return proc

consoleType = input("Create new console? (y/n) ")

runTypeError = True
while runTypeError:
    runType = input("Run code recursively? (y/n) ")
    if (runType == 'y'):
        cmdBase = "python recursive.py rec "
        with open('recursiveConfig.json') as f:
            configs = json.load(f)
        runTypeError = False
    elif (runType == 'n'):
        cmdBase = "python core.py core "
        with open('coreConfig.json') as f:
            configs = json.load(f)
        runTypeError = False
    else:
        print("Option not available. Please select (y/n).")

procs = []

runScript = True
while runScript:
    userAction = input("What do you want to do? ")

    if (userAction == 'exit'):
        for proc in procs:
            proc.terminate()
    
    aircraftTypeError = True
    while aircraftTypeError:
        aircraftType = input("Aircraft type to use: (none = all) ")
        if (aircraftType != ''):
            try:
                configs[aircraftType]
                aircraftTypeError = False
            except KeyError:
                print("Aircraft config does not exist")
                appendAircraftType = input("Would you like to add it? (y/n)")
                # TODO Create new config
                # TODO If user chooses not to add, list all existing and retry
        else:
            args = AEArgParser.createArgParser()
            forumSessidReq = api.get_page_session()
            worldReq, airlineDf = api.doLogin(args, forumSessidReq)
            phpSessidReq = api.doEnterWorld(args, airlineDf, worldReq)
            f = open('phpSessionReq.pickle', 'wb')
            f.write(pickle.dumps(phpSessidReq))
            f.close()
            cmdBase += '--pickled phpSessionReq.pickle '
            aircraftTypeError = False

    if (aircraftType == ''):
        for configsKey in configs:
            cmd = getCmd(cmdBase, configs[configsKey])
            proc = createSubProc(cmd)
            procs.append(proc)
    else:
        cmd = getCmd(cmdBase, configs[aircraftType])
        createSubProc(cmd)
