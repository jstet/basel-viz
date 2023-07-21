FROM postgres:latest
# copy init.sh to container
COPY ./init.sh docker-entrypoint-initdb.d/init.sh
RUN sed -i -e 's/\r$//' docker-entrypoint-initdb.d/init.sh
# copying data to container
RUN mkdir /data
RUN apt-get update && apt-get -y install wget
# downloading flows
RUN wget https://raw.githubusercontent.com/jstet/Basel_Convention_Scraper/main/output/processed/flows.csv -O /data/flows.csv
RUN wget https://raw.githubusercontent.com/jstet/Basel_Convention_Scraper/main/output/processed/countries.csv -O /data/countries.csv

