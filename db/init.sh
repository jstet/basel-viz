#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB"<<-EOSQL

 CREATE TABLE exports(
    id INT PRIMARY KEY,
    origin VARCHAR(2),
    destination VARCHAR(2),
    year INT,  
    amount FLOAT,
    UN1 BOOLEAN,
    UN3 BOOLEAN,
    UN4_1 BOOLEAN,
    UN4_2 BOOLEAN,
    UN4_3 BOOLEAN,
    UN5_1 BOOLEAN,
    UN5_2 BOOLEAN,
    UN6_1 BOOLEAN,
    UN6_2 BOOLEAN,

    UN8 BOOLEAN,
    UN9 BOOLEAN
    );
  
COPY exports(id, origin, destination, year, UN1,UN3,UN4_1,UN4_2,UN4_3,UN5_1,UN5_2,UN6_1,UN6_2,UN8,UN9,amount)
FROM '/data/flows.csv'
CSV HEADER DELIMITER ',';

 CREATE TABLE coords(
    country VARCHAR(2) PRIMARY KEY,
    lat FLOAT,
    lon FLOAT
    );
  
COPY coords(country, lat, lon)
FROM '/data/coords.csv'
CSV HEADER DELIMITER ',';
  
EOSQL
