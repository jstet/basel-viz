FROM postgres:15
COPY ./init.sh docker-entrypoint-initdb.d/init.sh
RUN sed -i -e 's/\r$//' docker-entrypoint-initdb.d/init.sh
RUN chmod +x /docker-entrypoint-initdb.d/init.sh
RUN mkdir /init_data
RUN apt-get update && apt-get -y install wget
RUN wget https://raw.githubusercontent.com/jstet/Basel_Convention_Scraper/main/output/processed/flows.csv -O /init_data/flows.csv
RUN wget https://raw.githubusercontent.com/jstet/Basel_Convention_Scraper/main/output/processed/countries.csv -O /init_data/countries.csv

