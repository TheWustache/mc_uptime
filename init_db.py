import sqlite3

db = sqlite3.connect('app/database.db')
c = db.cursor()

table_user = '''CREATE TABLE user (
  username TEXT PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  password TEXT NOT NULL,
  salt TEXT NOT NULL,
  admin INTEGER,
  can_vote INTEGER
)'''

table_app = '''CREATE TABLE app (
  id INTEGER PRIMARY KEY,
  name text,
  filepath text
)'''

table_availible = '''CREATE TABLE availible (
  id INTEGER PRIMARY KEY,
  slot_length INTEGER,
  user TEXT,
  app_id INTEGER,
  FOREIGN KEY(user) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY(app_id) REFERENCES app(id) ON UPDATE CASCADE ON DELETE CASCADE
)'''

table_slot = '''CREATE TABLE slot (
  id INTEGER PRIMARY KEY,
  day TEXT,
  start_time INTEGER,
  availible_id INTEGER,
  FOREIGN KEY(availible_id) REFERENCES availible(id) ON UPDATE CASCADE ON DELETE CASCADE
)'''

c.execute(table_user)
c.execute(table_app)
c.execute(table_availible)
c.execute(table_slot)

db.commit()

db.close()
