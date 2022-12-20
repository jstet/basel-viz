#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB"<<-EOSQL
  CREATE TABLE ycodes(
    ycode_id INT PRIMARY KEY);
  
  DO \$FN\$
  BEGIN
    FOR counter IN 1..49 LOOP
      RAISE NOTICE 'Counter: %', counter;
      EXECUTE format('ALTER TABLE ycodes ADD COLUMN Y%s BOOLEAN',counter) 
        USING counter;
    END LOOP;
  END;
  \$FN\$;

  CREATE TABLE exports(
    id INT PRIMARY KEY,
    ycode_id INT,
    amount INT,
    country_of_destination VARCHAR(2),
    country VARCHAR(100),
    year INT,
    CONSTRAINT fk_ycodes
      FOREIGN KEY(ycode_id) 
	      REFERENCES ycodes(ycode_id)
  );
  
EOSQL