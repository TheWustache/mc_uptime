from flask import session
import os.path
import os
from app.password import generate_salt, hash_password, check_password
from app.db import get_dbc

users_dir = os.path.join(os.curdir, 'app', 'users')


def login_user(username, password):
    """Logs in user. Return True if successful, False otherwise"""
    # stop if user doesn't exist
    # TODO: merge user doesn't exist and read user data -> one sql statement
    if not user_exists(username):
        return False

    # read user data
    db, c = get_dbc()
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


def is_admin(username):
    db, c = get_dbc()
    c.execute('''SELECT admin
        FROM user
        WHERE username = ?''',
              (username,))
    result = c.fetchone()
    return result['admin'] == 1


def user_has_app(username, app_id):
    db, c = get_dbc()
    c.execute('''SELECT count(*) AS count
        FROM availible
        WHERE user = ?
        AND app_id = ?''',
              (username, app_id))
    result = c.fetchone()
    return result['count'] > 0


def get_availible_id(username, app_id):
    db, c = get_dbc()
    c.execute('''SELECT id
        FROM availible
        WHERE user = ?
        AND app_id = ?''',
        (username, app_id))
    return c.fetchone()['id']


def user_exists(username):
    """Checks whether user exists. Returns True if yes, False otherwise"""
    db, c = get_dbc()

    # count all occurences of username
    c.execute(
        'SELECT COUNT(*) FROM user WHERE username = ? GROUP BY username', (username,))
    result = c.fetchone()

    # username should occur once if it exists, fetchone yields None if not
    return result is not None

def user_get_user_slot_ids(username, limit=3):
    """Return list of specified (default 3) amount of user_slot ids for user"""
    db, c = get_dbc()
    c.execute('''SELECT id
        FROM user_slot
        WHERE user = ?
        LIMIT ?''',
        (username, limit))
    return list(s['id'] for s in c.fetchall())


def create_user(username, firstname, lastname, password, admin=False, canVote=True):
    # secure password
    salt = generate_salt(32)
    secure_pw = hash_password(password, salt)

    # write to database
    db, c = get_dbc()
    c.execute('INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?)', (username,
                                                                firstname, lastname, secure_pw, salt, int(admin), int(canVote)))
    # create 3 user_slot entries
    c.executemany('''INSERT INTO user_slot
        VALUES (null, ?, null, 0)''',
        [(username,),(username,),(username,)])

    db.commit()
