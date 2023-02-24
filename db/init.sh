#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB"<<-EOSQL

 CREATE TABLE exports(
    id INT PRIMARY KEY,
    origin VARCHAR(2),
    destination VARCHAR(2),
    year INT,  
    UN1 FLOAT,
    UN3 FLOAT,
    UN4_1 FLOAT,
    UN4_2 FLOAT,
    UN4_3 FLOAT,
    UN5_1 FLOAT,
    UN5_2 FLOAT,
    UN6_1 FLOAT,
    UN6_2 FLOAT,
    UN8 FLOAT,
    UN9 FLOAT,
    unspecified FLOAT,
    multiple FLOAT
    );
  
COPY exports(id, origin, destination, year, UN1,UN3,UN4_1,UN4_2,UN4_3,UN5_1,UN5_2,UN6_1,UN6_2,UN8,UN9,unspecified,multiple)
FROM '/data/flows.csv'
CSV HEADER DELIMITER ',';

 CREATE TABLE coords(
    country VARCHAR(2) PRIMARY KEY,
    lat FLOAT,
    lon FLOAT,
    name VARCHAR(50),
    population INT
    );
  
COPY coords(country, lat, lon, name, population)
FROM '/data/coords.csv'
CSV HEADER DELIMITER ',';
  
EOSQL
