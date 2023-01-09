from sqlalchemy.orm import Session
from models import Export

def to_dct(res):
    lst = []
    for row in res:
        dct = row.__dict__
        dct.pop('_sa_instance_state')
        lst.append(dct)
    return lst



def query_get_all(db: Session):
    res = db.query(Export).all()
    lst = to_dct(res)
    print("done1")
    return lst

def query_country(db: Session, country):
    res = db.query(Export).filter(Export.country == country.upper()).all()
    lst = to_dct(res)
    print("done1")
    return lst

