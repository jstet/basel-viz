from sqlalchemy.orm import Session
from models import Export, Coord

def to_lst(res):
    lst = []
    for row in res:
        dct = dict(row.Export.__dict__, **row.Coord.__dict__)
        dct.pop('_sa_instance_state')
        dct.pop('country')
        lst.append(dct)
    return lst

def to_line(res, db):
    dct = {}
    dct["type"] = "FeatureCollection"
    lst = []
    for i in res:
        feature = {}
        feature["type"] = "Feature"
        feature["properties"] = i
        feature["properties"].pop("lat")
        feature["properties"].pop("lon")
        feature["geometry"] = {"type": "LineString", "coordinates": [[i["lat"], i["lon"]]]}
        lst.append(feature)
    dct["features"] = lst
    return dct

def query_get_all(db: Session):
    res = db.query(Export).all()
    lst = to_lst(res)
    return lst

def query_country(db: Session, c):
    flows = db.query(Export, Coord).filter(Export.origin == c).join(Export, Export.origin == Coord.country).all()
    dest_coords = db.query(Export, Coord).filter(Export.origin == c).join(Export, Export.destination == Coord.country).all()
    flows = to_line(to_lst(flows), db)

    return flows


    """
    with orig_coords as (SELECT * from  exports 
inner join coords  on exports.origin=coords.country), 
dest_coords as (SELECT * from  exports 
inner join coords  on exports.destination=coords.country)"""

