DROP TABLE IF EXISTS guests;

CREATE TABLE guests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  nick TEXT NOT NULL,
  message TEXT NOT NULL
);