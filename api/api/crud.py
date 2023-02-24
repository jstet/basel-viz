from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Export
from queries import bidirect_query, unidirect_query, points_query


def to_lst(res):
    lst = []
    for row in res:
        dct = dict(row["json_build_object"])
        lst.append(dct)
    return lst



def query_flows(db: Session, c, y):
    print(bidirect_query(y, c))
    bidirectional = to_lst(db.execute(text(bidirect_query(y, c))))
    unidirectional = to_lst(db.execute(text(unidirect_query(y, c))))
    
    return {"bidirectional": bidirectional, "unidirectional": unidirectional}


def query_points(db: Session, c, y):
    points = to_lst(db.execute(text(points_query)))
    return points
