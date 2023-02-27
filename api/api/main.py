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
lvl = "region|sub_region|country"

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ORJSON is faster than normal fastapi json


@app.get("/flows", response_class=ORJSONResponse)
def get_flows(s: Union[str, int, None] = Query(default=None, max_length=3), 
              y: List[int] = Query(None), 
              n: Union[bool, None] = Query(default=False), 
              l: Union[str, None] = Query(default='region', max_length=10, regex=lvl),
              db: Session = Depends(get_db)):
    results = query_flows(db, s=s, y=y, n=n, l=l)
    return ORJSONResponse(results)

@app.get("/points", response_class=ORJSONResponse)
def get_points(s: Union[str, int, None] = Query(default=None, max_length=3),
               y: List[int] = Query(None), 
               n: Union[bool, None] = Query(default=False),
               l: Union[str, None] = Query(default='region', max_length=10, regex=lvl),
               db: Session = Depends(get_db)):
    results = query_points(db, s=s, y=y, n=n, l=l)
    return ORJSONResponse(results)

@app.get("/countries", response_class=ORJSONResponse)
def get_countries(db: Session = Depends(get_db)):
    results = query_countries(db)
    return ORJSONResponse(results)


@app.get("/coords", response_class=ORJSONResponse)
def get_countries(db: Session = Depends(get_db),  l: Union[str, None] = Query(default='region', max_length=10, regex=lvl), d: Union[bool, None] = Query(default=False)):
    results = query_coords(db,l,d)
    return ORJSONResponse(results)

@app.get("/no_exports", response_class=ORJSONResponse)
def get_noExports(db: Session = Depends(get_db),  s: Union[str, int, None] = Query(default=None, max_length=3), l: Union[str, None] = Query(default='region', max_length=10),  y: List[int] = Query(None)):
    results = query_no_exports(db, l, y,s)
    return ORJSONResponse(results)

