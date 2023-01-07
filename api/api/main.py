import os
import uvicorn
import sys
import sqlalchemy
from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models 
from helpers import generate_model
from database import *

generate_model(engine=engine, metadata=metadata, outfile='models.py') 



app = FastAPI(title="FDS Statistics API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


    
@app.get("/")
def root():
    return "hu"


