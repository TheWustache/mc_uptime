import sqlite3
from app import app
from flask import g


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        #TODO: remove app/
        db = g._database = sqlite3.connect('app/database.db')
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
