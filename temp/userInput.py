from getpass import getpass

def setVar(args=None, varName=None, inputText=None):
    try:
        varValue = vars(args)[varName]
    except KeyError:
        if varName == 'password':
            varValue = getpass()
        else:
            varValue = input(inputText)
    return varValue
