### Tips for developing
After making changes to the databases setup code, run:
```
docker compose down --volumes
docker-compose up --build --force-recreate
```

You can start only the database with (while in root folder):
```
docker compose -f database.yml  up -d
```
After making changes to the databases setup code, run:
```
docker compose -f database.yml down --volumes
docker compose -f database.yml  up --build --force-recreate
```

