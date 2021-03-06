-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS comment;

CREATE TABLE user (
  -- required fields
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  dateOfBirth TEXT NOT NULL, -- YYYY-MM-DD
  password TEXT NOT NULL,
  admin INTEGER NOT NULL DEFAULT 0,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  -- optional fields for account info
  profilePic TEXT,
  email TEXT,
  firstName TEXT,
  bio TEXT,

  class_number TEXT,
  class_level TEXT,
  speciality TEXT,

  -- optional fields for social media
  -- store only the username/id not the full url
  facebook TEXT,
  twitter TEXT,
  instagram TEXT,
  linkedin TEXT,
  youtube TEXT,
  github TEXT,

  website TEXT
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  body TEXT NOT NULL,
  author_id INTEGER,
  reported TEXT, -- add id of reporter for every report
  status TEXT DEFAULT visible, -- visible, hidden, checked
  anonymous INTEGER NOT NULL DEFAULT 1,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  like TEXT,

  FOREIGN KEY (author_id) REFERENCES user (id) ON DELETE CASCADE -- # TODO test delete cascade
);

CREATE TABLE comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  text TEXT NOT NULL,
  post_id INTEGER NOT NULL,
  author_id INTEGER NOT NULL,
  anonymous INTEGER NOT NULL DEFAULT 1,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (author_id) REFERENCES user (id) ON DELETE CASCADE,
  FOREIGN KEY (post_id) REFERENCES post (id) ON DELETE CASCADE
);