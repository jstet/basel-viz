### Tips for developing
After making changes to the database setup code, run:
```
docker compose -f database.yml down --volumes
docker compose -f database.yml  up --build --force-recreate
```

You can start the database only with (while in root folder):
```
docker compose -f database.yml  up -d
```




