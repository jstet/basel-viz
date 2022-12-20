FROM postgres:latest
# copy init.sh to container
COPY ./init.sh docker-entrypoint-initdb.d/init.sh
# copying data to container
COPY ./data/imports.csv data/imports.csv
COPY ./data/exports.csv data/exports.csv
# copying postgres config to container
COPY ./postgresql.conf etc/postgresql/postgresql.conf
CMD ["-c", "config_file=/etc/postgresql/postgresql.conf"]