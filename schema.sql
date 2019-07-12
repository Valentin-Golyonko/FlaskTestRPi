-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS bme280;

CREATE TABLE bme280
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature NUMERIC   NOT NULL,
    humidity    NUMERIC   NOT NULL,
    pressure    NUMERIC   NOT NULL,
    created     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
