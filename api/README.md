## Set up
1. Create new environment 
2. Activate environment
3. Install requirements

For windows:
```
python -m venv venv
./venv/Scripts/activate
python -m pip install -r requirements.txt
```

4. Create .env file
```
POSTGRES_URL=postgresql://postgres:postgres@localhost:5434/main
```

## Starting API
1. Start DB

```
docker compose -f database.yml build 
docker compose -f database.yml  up 
```
2. Start API (while in api/api folder)
```
uvicorn main:app --reload
```

## Refreshing models
With an activated environment and while in the API subfolder:
```
python create_models.py
```

