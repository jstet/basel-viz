#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB"<<-EOSQL
  CREATE TABLE y_codes(
    y_code_id INT PRIMARY KEY);
  
  DO \$FN\$
  BEGIN
    FOR counter IN 1..49 LOOP
      RAISE NOTICE 'Counter: %', counter;
      EXECUTE format('ALTER TABLE y_codes ADD COLUMN Y%s BOOLEAN',counter) 
        USING counter;
    END LOOP;
  END;
  \$FN\$;

  CREATE TABLE annex_3(
    annex_3_id INT PRIMARY KEY,
    "h1" BOOLEAN,
    "h3" BOOLEAN,
    "h4.1" BOOLEAN,
    "h4.2" BOOLEAN,
    "h4.3" BOOLEAN,
    "h5.1" BOOLEAN,
    "h5.2" BOOLEAN,
    "h6.1" BOOLEAN,
    "h6.2" BOOLEAN,
    "h8" BOOLEAN,
    "h10" BOOLEAN,
    "h11" BOOLEAN,
    "h12" BOOLEAN,
    "h13" BOOLEAN);

  CREATE TABLE annex_4_a(
    annex_4_a_id INT PRIMARY KEY,
    D1 BOOLEAN,
    D2 BOOLEAN,
    D3 BOOLEAN,
    D4 BOOLEAN,
    D6 BOOLEAN,
    D7 BOOLEAN,
    D8 BOOLEAN,
    D9 BOOLEAN,
    D10 BOOLEAN,
    D11 BOOLEAN,
    D12 BOOLEAN,
    D13 BOOLEAN,
    D14 BOOLEAN,
    D15 BOOLEAN);
  
  CREATE TABLE annex_4_b(
    annex_4_b_id INT PRIMARY KEY,
    R1 BOOLEAN,
    R2 BOOLEAN,
    R3 BOOLEAN,
    R4 BOOLEAN,
    R6 BOOLEAN,
    R7 BOOLEAN,
    R8 BOOLEAN,
    R9 BOOLEAN,
    R10 BOOLEAN,
    R11 BOOLEAN,
    R12 BOOLEAN,
    R13 BOOLEAN);
  
  CREATE TABLE exports(
    id INT PRIMARY KEY,
    annex_3_id INT,
    annex_4_a_id INT,
    annex_4_b_id INT,
    amount INT,
    country_of_destination VARCHAR(2),
    country VARCHAR(100),
    year INT,
    CONSTRAINT fk_annex_3
      FOREIGN KEY(annex_3_id) 
	      REFERENCES annex_3(annex_3_id)
    ,
    CONSTRAINT fk_annex_4_a
      FOREIGN KEY(annex_4_a_id) 
	      REFERENCES annex_4_a(annex_4_a_id)
    ,
    CONSTRAINT fk_annex_4_b
      FOREIGN KEY(annex_4_b_id) 
	      REFERENCES annex_4_b(annex_4_b_id)
    );
  
EOSQL