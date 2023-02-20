## Setup
1. First, create a .env file with follwing contents:
```
API_URL=http://localhost:8000
```
2. Then, u gotta start the API and the DB. 

```
docker compose -f api.yml  up 
```
3. Install packages;
```
npm install
```
4. Then, run the sveltekit project with:
```
npm run dev
```

After making changes to the API or the DB run:
```
docker compose -f api.yml down --volumes
docker compose -f api.yml  up --build --force-recreate
```
