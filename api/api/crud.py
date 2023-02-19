from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Export


def to_lst(res):
    lst = []
    for row in res:
        dct = dict(row["json_build_object"])
        lst.append(dct)
    return lst


def query_flows(db: Session, c):
    query = f"""
with t as (
select
	origin,
	destination,
	SUM(un1) as un1,
	SUM(un3) as un3,
	SUM(un4_1) as un4_1,
	SUM(un4_2) as un4_2,
	SUM(un4_3) as un4_3,
	SUM(un5_1) as un5_1,
	SUM(un5_2) as un5_2,
	SUM(un6_1) as un6_1,
	SUM(un6_2) as un6_2,
	SUM(un8) as un8,
	SUM(un9) as un9,
	SUM(unspecified) as unspecified,
	SUM(multiple) as multiple 
from
	exports
group by
	origin,
	destination
	)

select
	json_build_object(
    	'origin_code', t.origin,
    	'destination_code', t.destination,
        'un_classes', json_build_array(
         json_build_array('label', 'UN_1', 'value', t.un1),
         json_build_array('label', 'UN_3', 'value', t.un3),
         json_build_array('label', 'UN_4_1', 'value', t.un1),
         json_build_array('label', 'UN_4_2', 'value', t.un1),
         json_build_array('label', 'UN_4_3', 'value', t.un1),
         json_build_array('label', 'UN_5_1', 'value', t.un1),
         json_build_array('label', 'UN_6_1', 'value', t.un1),
         json_build_array('label', 'UN_6_2', 'value', t.un1),
         json_build_array('label', 'UN_8', 'value', t.un1),
         json_build_array('label', 'UN_9', 'value', t.un1),
         json_build_array('label', 'unspecified', 'value', t.unspecified),
         json_build_array('label', 'multiple', 'value', t.multiple)
     	
       )
     )
from
	t
where
	origin = '{c}';
"""

    flows = to_lst(db.execute(text(query)))
    print(flows)
    return flows

def query_points(db: Session, c):
    query = f"""
with t as (
select
	origin,
	destination,
	SUM(un1) as un1,
	SUM(un3) as un3,
	SUM(un4_1) as un4_1,
	SUM(un4_2) as un4_2,
	SUM(un4_3) as un4_3,
	SUM(un5_1) as un5_1,
	SUM(un5_2) as un5_2,
	SUM(un6_1) as un6_1,
	SUM(un6_2) as un6_2,
	SUM(un8) as un8,
	SUM(un9) as un9,
	SUM(unspecified) as unspecified,
	SUM(multiple) as multiple 
from
	exports
group by
	origin,
	destination
	)

select
	json_build_object(
    	'origin_code', t.origin,
    	'destination_code', t.destination,
        'un_classes', json_build_array(
         json_build_array('label', 'UN_1', 'value', t.un1),
         json_build_array('label', 'UN_3', 'value', t.un3),
         json_build_array('label', 'UN_4_1', 'value', t.un1),
         json_build_array('label', 'UN_4_2', 'value', t.un1),
         json_build_array('label', 'UN_4_3', 'value', t.un1),
         json_build_array('label', 'UN_5_1', 'value', t.un1),
         json_build_array('label', 'UN_6_1', 'value', t.un1),
         json_build_array('label', 'UN_6_2', 'value', t.un1),
         json_build_array('label', 'UN_8', 'value', t.un1),
         json_build_array('label', 'UN_9', 'value', t.un1),
         json_build_array('label', 'unspecified', 'value', t.unspecified),
         json_build_array('label', 'multiple', 'value', t.multiple)
     	
       )
     )
from
	t
where
	origin = '{c}';
"""

    flows = to_lst(db.execute(text(query)))
    print(flows)
    return flows
