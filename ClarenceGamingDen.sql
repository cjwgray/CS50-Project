CREATE TABLE users(id INTEGER NOT NULL PRIMARY KEY, username TEXT NOT NULL, hash TEXT NOT NULL);

CREATE TABLE comments(id INTEGER NOT NULL PRIMARY KEY, username TEXT NOT NULL, send TEXT, output TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE post(id INTEGER NOT NULL PRIMARY KEY, title TEXT NOT NULL, body TEXT NOT NULL, date INTEGER NOT NULL);