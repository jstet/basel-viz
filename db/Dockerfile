FROM postgres:latest
# copy init.sh to container
COPY ./init.sh docker-entrypoint-initdb.d/init.sh
# copying data to container
RUN mkdir /data
RUN apt-get update && apt-get -y install wget
RUN wget https://raw.githubusercontent.com/jstet/Basel_Convention_Scraper/main/output/processed/clean.csv -O /data/exports.csv
# copying postgres config to container
COPY ./postgresql.conf etc/postgresql/postgresql.conf
CMD ["-c", "config_file=/etc/postgresql/postgresql.conf"]