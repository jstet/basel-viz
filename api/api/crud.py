from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Export
from queries import *


def to_lst(res):
    lst = []
    for row in res:
        dct = dict(row["json_build_object"])
        lst.append(dct)
    return lst



def query_flows(db: Session, c, y, n, l):
    bidirectional = to_lst(db.execute(text(bidirect_query( c=c, y=y, n=n, l=l))))
    unidirectional = to_lst(db.execute(text(unidirect_query( c=c, y=y, n=n, l=l))))    
    return {"bidirectional": bidirectional, "unidirectional": unidirectional}


def query_points(db: Session, c, y, n, l):
    points = to_lst(db.execute(text(points_query( c=c, y=y, n=n, l=l))))
    return points


def query_countries(db: Session):
    countries = to_lst(db.execute(text(countries_query())))
    return countries

def  query_coords(db:Session, l):
    coords = to_lst(db.execute(text(coords_query(l))))
    return coords
