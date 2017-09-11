from app import app
from flask import session
import os.path
import os
import json

users_dir = os.path.join(os.curdir, 'app', 'users')

def login_user(username, password):
    """Logs in user. Return True if successful, False otherwise"""
    # stop if user doesn't exist
    if not user_exists(username):
        return False

    # read user data
    f = open(os.path.join(users_dir, username + '.json'))
    user = json.load(f)

    # check if password matches
    # TODO: actually make password secure
    if password == user['password']:
        session['username'] = username
        print("%s successful login" % username)
        return True
    else:
        return False


def logout_user():
    """Logs out user"""
    session.pop('username', None)


def user_exists(username):
    """Checks whether user exists. Returns True if yes, False otherwise"""
    # users are implicitly listed in file names
    # TODO: make directory with users configurable
    files = os.listdir(os.path.join(users_dir))
    if files:
        for user in files:
            if (username + '.json') == user:
                return True
    return False


def create_user():
    def generate_user_file(username, firstname, lastname, password, slotLength, canVote="false", rank="0"):
        user = {
            'username': username,
            'firstname': firstname,
            'lastname': lastname,
            'password': "hash",
            'salt': "salt",
            'availibleTimes': {
                'length': slotLength,
                'slots': [
                    {
                        'day': 0,
                        'slot': 0
                    },
                    {
                        'day': 1,
                        'slot': 0
                    },
                    {
                        'day': 2,
                        'slot': 0
                    }
                ]
            },
            'canVote': canVote,
            'rank': rank
        }


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        if user_exists(sys.argv[1]):
            print(sys.argv[1] + " exists!")
        else:
            print(sys.argv[1] + " does not exist!")
