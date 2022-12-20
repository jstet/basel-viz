### Tips for developing
After making chnages to the databases setup code, run:
```
docker compose down --volumes
docker-compose up --build --force-recreate
```
