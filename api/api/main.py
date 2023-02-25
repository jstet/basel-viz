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

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ORJSON is faster than normal fastapi json


@app.get("/flows", response_class=ORJSONResponse)
def get_flows(c: Union[str, None] = Query(default=None, max_length=2), 
              y: List[int] = Query(None), 
              n: Union[bool, None] = Query(default=False), 
              l: Union[int, None] = Query(default=0),
              db: Session = Depends(get_db)):
    if c!=None:
        l=0
    results = query_flows(db,  c=c, y=y, n=n, l=l)
    return ORJSONResponse(results)


@app.get("/points", response_class=ORJSONResponse)
def get_points(c: Union[str, None] = Query(default=None, max_length=2),
               y: List[int] = Query(None), 
               n: Union[bool, None] = Query(default=False),
               l: Union[int, None] = Query(default=0),
               db: Session = Depends(get_db)):
    if c!=None:
        l=0
    results = query_points(db, c=c, y=y, n=n, l=l)
    return ORJSONResponse(results)

@app.get("/countries", response_class=ORJSONResponse)
def get_countries(db: Session = Depends(get_db)):
    results = query_countries(db)
    return ORJSONResponse(results)


@app.get("/coords", response_class=ORJSONResponse)
def get_countries(db: Session = Depends(get_db),  l: Union[int, None] = Query(default=0)):
    results = query_coords(db,l)
    return ORJSONResponse(results)
