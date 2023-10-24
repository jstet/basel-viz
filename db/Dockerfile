FROM postgres:15

# Copy the init.sh script and set permissions
COPY ./init.sh /docker-entrypoint-initdb.d/init.sh
RUN chmod +x /docker-entrypoint-initdb.d/init.sh
RUN sed -i -e 's/\r$//' docker-entrypoint-initdb.d/init.sh

# Create a directory for data
RUN mkdir /init_data

# Install wget
RUN apt-get update && apt-get -y install wget

# Download data files
RUN wget -O /init_data/flows.csv https://raw.githubusercontent.com/jstet/Basel_Convention_Scraper/main/output/processed/flows.csv
RUN wget -O /init_data/countries.csv https://raw.githubusercontent.com/jstet/Basel_Convention_Scraper/main/output/processed/countries.csv