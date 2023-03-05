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

def to_obj(x):
    obj = {}
    for i in x:
        key = list(i.keys())[0]
        obj[key] = i[key]
    return obj

def query_flows(db: Session, s, y, n, l, u):
    bidirectional = to_lst(db.execute(text(bidirect_query(s=s, y=y, n=n, l=l, u=u))))
    unidirectional = to_lst(db.execute(text(unidirect_query(s=s, y=y, n=n, l=l, u=u)))) 
    print(unidirect_query(s=s, y=y, n=n, l=l, u=u))   
    return {"bidirectional": bidirectional, "unidirectional": unidirectional}


def query_points(db: Session, s, y, n, l, u):
    points = to_lst(db.execute(text(points_query(s=s, y=y, n=n, l=l, u=u))))
    return points


def query_countries(db: Session):
    countries = to_lst(db.execute(text(countries_query())))
    return to_obj(countries)


def  query_coords(db:Session, l,d):
    coords = to_lst(db.execute(text(coords_query(l,d))))
    return to_obj(coords)

def  query_no_exports(db:Session, l, y, s, u):
    coords = to_lst(db.execute(text(no_exports_query(l, y,s, u))))
    return coords
