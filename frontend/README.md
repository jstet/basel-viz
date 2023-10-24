## Setup
1. First, create a .env file with following contents:
```
PUBLIC_API_URL=http://localhost:3000


```
2. Then, start the API and the DB. 

```
docker compose -f api.yml  up 
```
3. Then, run the Svelte Kit project with:
```
npm run dev
```

After making changes to the API or the DB run:
```
docker compose -f api.yml down --volumes
docker compose -f api.yml build --no-cache 
docker compose -f api.yml  up --force-recreate
```
