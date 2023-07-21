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
FROM '/init_data/flows.csv'
CSV HEADER DELIMITER ',';

 CREATE TABLE countries(
    code VARCHAR(2) PRIMARY KEY,
    name VARCHAR(50),
    lat FLOAT,
    lon FLOAT,
    region_code INT,
    region_name VARCHAR(50),
    region_lat FLOAT,
    region_lon FLOAT,
    sub_region_code INT,
    sub_region_name VARCHAR(50),
    sub_region_lat FLOAT,
    sub_region_lon FLOAT,
    hdi_code VARCHAR(50),
    hdi_name VARCHAR(50),
    hdi_lat FLOAT,
    hdi_lon FLOAT,
    population INT,
    destination_only BOOLEAN
    );
  
COPY countries(code,name,lat,lon,region_code,region_name,region_lat,region_lon,sub_region_code,sub_region_name, sub_region_lat, sub_region_lon, hdi_code, hdi_name, hdi_lat, hdi_lon, population, destination_only)
FROM '/init_data/countries.csv'
CSV HEADER DELIMITER ',';
  
EOSQL
