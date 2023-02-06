from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Export, Coord


def to_lst(res):
    lst = []
    for row in res:
        dct = dict(row)
        lst.append(dct)
    return lst


def to_line(res, db):
    dct = {}
    dct["type"] = "FeatureCollection"
    lst = []
    for i in res:
        print(i)
        feature = {}
        feature["type"] = "Feature"
        feature["properties"] = dict(i)
        feature["properties"].pop("origin_lat")
        feature["properties"].pop("origin_lon")
        feature["properties"].pop("destination_lat")
        feature["properties"].pop("destination_lon")
        feature["geometry"] = {"type": "LineString",
                               "coordinates": [[i["origin_lat"], i["origin_lon"]],[i["destination_lat"],i["destination_lon"]]]}
        lst.append(feature)
    dct["features"] = lst
    return dct


def query_get_all(db: Session):
    res = db.query(Export).all()
    lst = to_lst(res)
    return lst


def query_country(db: Session, c):
    query = f"""
with temp_table1 as (
select
	*
from
	exports
inner join coords on
	exports.origin = coords.country),
temp_table2 as (
select
	*
from
	exports
inner join coords on
	exports.destination = coords.country)
select
	temp_table1.id,
	temp_table1.origin,
	temp_table1.destination,
	temp_table1."year",
	temp_table1.amount,
	temp_table1.un1,
	temp_table1.un3,
	temp_table1.un4_1,
	temp_table1.un4_2,
	temp_table1.un4_3,
	temp_table1.un5_1,
	temp_table1.un5_2,
	temp_table1.un6_1,
	temp_table1.un6_2,
	temp_table1.un8,
	temp_table1.un9,
	temp_table1.lat as origin_lat,
	temp_table1.lon as origin_lon,
	temp_table2.lat as destination_lat,
	temp_table2.lon as destination_lon
from
	temp_table2
inner join temp_table1 on
	temp_table2.id = temp_table1.id
where temp_table1.origin = '{c}';
"""

    flows = db.execute(text(query))

    # flows = db.query(Export, Coord).filter(Export.origin == c).join(
    #     Export, Export.origin == Coord.country).all()
    flows = to_line(to_lst(flows), db)

    return flows

