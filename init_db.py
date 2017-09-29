import sqlite3

db = sqlite3.connect('app/database.db')
c = db.cursor()

try:
    c.executescript(open('schema.sql').read())
    db.commit()
    print("Successfully initiated database.")
    try:
        # initialize settings
        c.executescript(open('settings.sql').read())
        db.commit()
        print("Successfully initiated settings.")
    except sqlite3.DatabaseError as er:
        print("Failed to initialize settings.")
        print(er)
except sqlite3.DatabaseError as er:
    print("Database initialization has failed.")
    print(er)

db.close()
