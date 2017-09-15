CREATE TABLE user (
  username TEXT PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  password TEXT NOT NULL,
  salt TEXT NOT NULL,
  admin INTEGER,
  can_vote INTEGER
);

CREATE TABLE app (
  id INTEGER PRIMARY KEY,
  name TEXT,
  filepath TEXT,
  next_day TEXT,
  next_slot INTEGER,
  slot_length INTEGER
);

CREATE TABLE availible (
  id INTEGER PRIMARY KEY,
  user TEXT,
  app_id INTEGER,
  FOREIGN KEY(user) REFERENCES user(username) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY(app_id) REFERENCES app(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE slot (
  id INTEGER PRIMARY KEY,
  day TEXT,
  start_time INTEGER,
  availible_id INTEGER,
  FOREIGN KEY(availible_id) REFERENCES availible(id) ON UPDATE CASCADE ON DELETE CASCADE
);
