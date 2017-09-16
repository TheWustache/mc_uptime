from flask import session
import os.path
import os
import json
from app.password import generate_salt, hash_password, check_password
from app.db import get_db

users_dir = os.path.join(os.curdir, 'app', 'users')


def login_user(username, password):
    """Logs in user. Return True if successful, False otherwise"""
    # stop if user doesn't exist
    #TODO: merge user doesn't exist and read user data -> one sql statement
    if not user_exists(username):
        return False

    # read user data
    db = get_db()
    c = db.cursor()
    c.execute('SELECT password, salt FROM user WHERE username = ?', (username,))
    result = c.fetchone()

    # check if password matches
    if check_password(password, result['salt'], result['password']):
        # TODO: Consider saving logged in unser on server instead of clientside
        session['username'] = username
        print("%s successful login" % username)
        return True
    else:
        print("%s attempted login" % username)
        return False


def logout_user():
    """Logs out user"""
    session.pop('username', None)

def loggedin():
    return 'username' in session


def user_exists(username):
    """Checks whether user exists. Returns True if yes, False otherwise"""
    db = get_db()
    c = db.cursor()

    # count all occurences of username
    c.execute('SELECT COUNT(*) FROM user WHERE username = ? GROUP BY username', (username,))
    result = c.fetchone()

    # username should occur once if it exists, fetchone yields None if not
    return result is not None


def create_user(username, firstname, lastname, password, admin=False, canVote=True):
    # secure password
    salt = generate_salt(32)
    secure_pw = hash_password(password, salt)

    # write to database
    db = get_db()
    c = db.cursor()
    c.execute('INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?)', (username, firstname, lastname, secure_pw, salt, int(admin), int(canVote)))
    db.commit()
