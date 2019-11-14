import argparse

def createArgParser():
    parser = argparse.ArgumentParser(description='Airline empire CLI tool')
    subparsers = parser.add_subparsers(title='CLI commands',
                                    description='Sets program to parse args',
                                    help='Sets program to parse args instead of waiting for user input')

    # create the parser for the "core" command
    coreParser = subparsers.add_parser('core')
    coreParser.add_argument('--pickled', help='Used pickled session')
    coreParser.add_argument('--username', required=True, help='Username')
    coreParser.add_argument('--password', required=True, help='Password')
    coreParser.add_argument('--airline', required=True, help='Airline name')
    coreParser.add_argument('--country', help='Flight country')
    coreParser.add_argument('--region', help='Flight region')
    coreParser.add_argument('--reqRW', type=int, help='Minimum runway length')
    coreParser.add_argument('--rgMin', type=int, help='Flight minimum range')
    coreParser.add_argument('--rgMax', type=int, help='Flight maximum range')
    coreParser.add_argument('--depAirportCode', required=True, help='Departure airport code')
    coreParser.add_argument('--aircraftType', required=True, help='Aircraft type')
    coreParser.add_argument('--reducedCapacity', help='Flights over intended range')
    coreParser.add_argument('--autoSlots', help='Automatically buy slots')
    coreParser.add_argument('--autoTerminal', help='Automatically build terminal')
    coreParser.add_argument('--autoHub', help='Automatically create hub')
    coreParser.add_argument('--minFreq', type=int, help='Min frequency')
    coreParser.add_argument('--maxFreq', type=int, help='Max frequency')

    # create the parser for the "recursive" command
    recursiveParser = subparsers.add_parser('rec')
    recursiveParser.add_argument('--pickled', help='Used pickled session')
    recursiveParser.add_argument('--username', required=True, help='Username')
    recursiveParser.add_argument('--password', required=True, help='Password')
    recursiveParser.add_argument('--airline', required=True, help='Airline name')
    recursiveParser.add_argument('--recursion', help='Airline name')
    recursiveParser.add_argument('--reqRW', type=int, help='Minimum runway length')
    recursiveParser.add_argument('--rgMax', type=int, help='Flight maximum range')
    recursiveParser.add_argument('--depAirportCode', required=True, help='Departure airport code')
    recursiveParser.add_argument('--aircraftType', required=True, help='Aircraft type')
    recursiveParser.add_argument('--reducedCapacity', help='Flights over intended range')
    recursiveParser.add_argument('--autoSlots', help='Automatically buy slots')
    recursiveParser.add_argument('--autoTerminal', help='Automatically build terminal')
    recursiveParser.add_argument('--autoHub', help='Automatically create hub')
    recursiveParser.add_argument('--minFreq', type=int, help='Min frequency')
    recursiveParser.add_argument('--maxFreq', type=int, help='Max frequency')

    args = parser.parse_args()
    return args
