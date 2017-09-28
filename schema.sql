CREATE TABLE user (
  username TEXT PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  password TEXT NOT NULL,
  salt TEXT NOT NULL,
  admin INTEGER,
  can_vote INTEGER
);

CREATE TABLE user_slot (
  id INTEGER PRIMARY KEY,
  user TEXT,
  slot_id INTEGER,
  day TEXT,
  FOREIGN KEY(user) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY(slot_id) REFERENCES slot(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE slot (
  id INTEGER PRIMARY KEY,
  start_time INTEGER
);
