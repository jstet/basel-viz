import os
import uvicorn
import sys
import sqlalchemy
from typing import Union
from fastapi import FastAPI, status, Depends, Query
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import *
from crud import *
from models import *
from schemas import *


app = FastAPI(title="basel_viz")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ORJSON is faster than normal fastapi json 
    
@app.get("/flows", response_class=ORJSONResponse)
def get_flows(c: Union[str, None] = Query(default=None, max_length=2), y: List[int] = Query(None),  db: Session = Depends(get_db)):
    results = query_flows(db, c, y)
    return ORJSONResponse(results)

@app.get("/points",response_class=ORJSONResponse)
def get_points(c: Union[str, None] = Query(default=None, max_length=2), y: List[int] = Query(None), db: Session = Depends(get_db)):
    results = query_points(db, c, y)
    return ORJSONResponse(results)



