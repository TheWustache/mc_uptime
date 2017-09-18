import sqlite3
from app import app
from flask import g


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('app/database.db')
        db.row_factory = dict_factory
        c = db.cursor()
        c.execute('PRAGMA foreign_keys = ON')
    return db


def get_dbc():
    """Returns db with cursor"""
    db = get_db()
    return (db, db.cursor())


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
