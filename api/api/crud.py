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



def query_flows(db: Session, s, y, n, l):
    bidirectional = to_lst(db.execute(text(bidirect_query(s=s, y=y, n=n, l=l))))
    unidirectional = to_lst(db.execute(text(unidirect_query(s=s, y=y, n=n, l=l))))    
    return {"bidirectional": bidirectional, "unidirectional": unidirectional}


def query_points(db: Session, s, y, n, l):
    points = to_lst(db.execute(text(points_query(s=s, y=y, n=n, l=l))))
    return points


def query_countries(db: Session):
    countries = to_lst(db.execute(text(countries_query())))
    obj = {}
    for i in countries:
        key = list(i.keys())[0]

        obj[key] = i[key]

    return obj


def  query_coords(db:Session, l):
    coords = to_lst(db.execute(text(coords_query(l))))
    obj = {}
    for i in coords:
        key = list(i.keys())[0]

        obj[key] = i[key]

    return obj

def  query_noExports(db:Session, l, y):
    coords = to_lst(db.execute(text(noExports_query(l, y))))
    obj = {}
    for i in coords:
        key = list(i.keys())[0]

        obj[key] = i[key]

    return obj