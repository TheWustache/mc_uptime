import sqlite3

db = sqlite3.connect('app/database.db')
c = db.cursor()

try:
    c.executescript(open('schema.sql').read())
    db.commit()
    print("Successfully initiated database.")
except sqlite3.DatabaseError:
    print("Database initialization has failed.")

db.close()
