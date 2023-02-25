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

 CREATE TABLE countries(
    country VARCHAR(2) PRIMARY KEY,
    lat_0 FLOAT,
    lon_0 FLOAT,
    name VARCHAR(50),
    population INT,
    label_1 INT,
    lat_1 FLOAT,
    lon_1 FLOAT,
    label_2 INT,
    lat_2 FLOAT,
    lon_2 FLOAT,
    label_3 INT,
    lat_3 FLOAT,
    lon_3 FLOAT,
    label_4 INT,
    lat_4 FLOAT,
    lon_4 FLOAT,
    label_5 INT,
    lat_5 FLOAT,
    lon_5 FLOAT
    );
  
COPY countries(country, lat_0, lon_0, name, population, label_1, lat_1, lon_1, label_2, lat_2, lon_2, label_3, lat_3, lon_3, label_4, lat_4, lon_4, label_5, lat_5, lon_5)
FROM '/data/countries.csv'
CSV HEADER DELIMITER ',';
  
EOSQL
