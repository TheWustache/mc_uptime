from app.user import create_user
import sys
from flask import Flask


# fuck yeah stackoverflow
def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        # Reduce the argument list by copying it starting from index 1.
        argv = argv[1:]
    return opts

def strtobool(s):
    if s in ('True', 'true', 'T', 't', '0', '1', 'yeah'):
        return True
    else:
        return False


app = Flask(__name__)
with app.app_context():
    # username and password are necessary
    if '-u' not in sys.argv:
        print('Username missing!')
    elif '-p' not in sys.argv:
        print('Password missing!')
    else:
        # defaults
        u = {
            '-fn': 'Unspecified',
            '-ln': 'McUnspecified',
            '-a': 'False',
            '-v': 'False'
        }
        # convert boolean args to actual boolean
        u.update(getopts(sys.argv))
        u['-a'] = strtobool(u['-a'])
        u['-v'] = strtobool(u['-v'])

        create_user(u['-u'], u['-fn'], u['-ln'], u['-p'], u['-a'], u['-v'])
        print("Successfully created user " + u['-u'])
