-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS bme280;
DROP TABLE IF EXISTS owm;
DROP TABLE IF EXISTS twee;

CREATE TABLE bme280
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature NUMERIC   NOT NULL,
    humidity    NUMERIC   NOT NULL,
    pressure    NUMERIC   NOT NULL,
    created     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE owm
(
    weather_id  INTEGER NOT NULL,
    description TEXT    NOT NULL,
    icon        TEXT    NOT NULL,
    temp        NUMERIC NOT NULL,
    pressure    NUMERIC NOT NULL,
    humidity    NUMERIC NOT NULL,
    temp_min    NUMERIC NOT NULL,
    temp_max    NUMERIC NOT NULL,
    wind_speed  NUMERIC NOT NULL,
    wind_deg    NUMERIC NOT NULL,
    wind_gust   NUMERIC NOT NULL,
    time_unix   INTEGER NOT NULL
);

CREATE TABLE twee
(
    created_at     TEXT NOT NULL,
    user_name      TEXT NOT NULL,
    full_text      TEXT NOT NULL,
    media_url      TEXT NOT NULL,
    user_image_url TEXT NOT NULL
);