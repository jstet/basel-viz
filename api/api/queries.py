def handle_c(c):
    if c is None:
        where = ""
    else:
        where = f"""
         where
        origin = '{c}';
        """
    return where


def handle_y(y):
    if y is None:
        where = ""
    else:
        where = f"""
         where
            year between {y[0]} and {y[1]}
        """
    return where


def unidirect_query(y,c):
    return f"""
    with t1 as (
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
{handle_y(y)}
group by
	origin,
	destination
        ),
        
    bidirect as (
		select
			t1.origin,
			t1.destination,
			t1.un1,
			t1.un3,
			t1.un4_1,
			t1.un4_2,
			t1.un4_3,
			t1.un5_1,
			t1.un5_2,
			t1.un6_1,
			t1.un6_2,
			t1.un8,
			t1.un9,
			t1.unspecified,
			t1.multiple 
		from
			t1 as t3
		join t1 on
			t1.origin = t3.destination and t1.destination = t3.origin),

	unidirect as(
select
	*
from
	t1
except
select * from bidirect	
	)
    

	select
        json_build_object(
            'origin_code', unidirect.origin,
            'destination_code', unidirect.destination,
            'un_classes', json_build_array(
            json_build_object('label', 'UN_1', 'value', unidirect.un1),
            json_build_object('label', 'UN_3', 'value', unidirect.un3),
            json_build_object('label', 'UN_4_1', 'value', unidirect.un4_1),
            json_build_object('label', 'UN_4_2', 'value', unidirect.un4_2),
            json_build_object('label', 'UN_4_3', 'value', unidirect.un4_3),
            json_build_object('label', 'UN_5_1', 'value', unidirect.un5_1),
            json_build_object('label', 'UN_6_1', 'value', unidirect.un6_1),
            json_build_object('label', 'UN_6_2', 'value', unidirect.un6_2),
            json_build_object('label', 'UN_8', 'value', unidirect.un8),
            json_build_object('label', 'UN_9', 'value', unidirect.un9),
            json_build_object('label', 'unspecified', 'value', unidirect.unspecified),
            json_build_object('label', 'multiple', 'value', unidirect.multiple)
            
        )
        )
    from
        unidirect
    {handle_c(c)};
    """

def bidirect_query(y,c):
    return f"""
    with t1 as (
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

{handle_y(y)}
group by
	origin,
	destination
        ),
        
    bidirect as (
		select
			t1.origin,
			t1.destination,
			t1.un1,
			t1.un3,
			t1.un4_1,
			t1.un4_2,
			t1.un4_3,
			t1.un5_1,
			t1.un5_2,
			t1.un6_1,
			t1.un6_2,
			t1.un8,
			t1.un9,
			t1.unspecified,
			t1.multiple 
		from
			t1 as t3
		join t1 on
			t1.origin = t3.destination and t1.destination = t3.origin)
    

	select
        json_build_object(
            'origin_code', bidirect.origin,
            'destination_code', bidirect.destination,
            'un_classes', json_build_array(
            json_build_object('label', 'UN_1', 'value', bidirect.un1),
            json_build_object('label', 'UN_3', 'value', bidirect.un3),
            json_build_object('label', 'UN_4_1', 'value', bidirect.un4_1),
            json_build_object('label', 'UN_4_2', 'value', bidirect.un4_2),
            json_build_object('label', 'UN_4_3', 'value', bidirect.un4_3),
            json_build_object('label', 'UN_5_1', 'value', bidirect.un5_1),
            json_build_object('label', 'UN_6_1', 'value', bidirect.un6_1),
            json_build_object('label', 'UN_6_2', 'value', bidirect.un6_2),
            json_build_object('label', 'UN_8', 'value', bidirect.un8),
            json_build_object('label', 'UN_9', 'value', bidirect.un9),
            json_build_object('label', 'unspecified', 'value', bidirect.unspecified),
            json_build_object('label', 'multiple', 'value', bidirect.multiple)
            
        )
        )
    from
        bidirect
    {handle_c(c)};
    """

def points_query(y,c):
    return f"""
with t as (
select
    origin,
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
{handle_y(y)}
group by
    origin
    )

select
    json_build_object(
        'origin_code', t.origin,
        'un_classes', json_build_array(
        json_build_object('label', 'UN_1', 'value', t.un1),
        json_build_object('label', 'UN_3', 'value', t.un3),
        json_build_object('label', 'UN_4_1', 'value', t.un4_1),
        json_build_object('label', 'UN_4_2', 'value', t.un4_2),
        json_build_object('label', 'UN_4_3', 'value', t.un4_3),
        json_build_object('label', 'UN_5_1', 'value', t.un5_1),
        json_build_object('label', 'UN_6_1', 'value', t.un6_1),
        json_build_object('label', 'UN_6_2', 'value', t.un6_2),
        json_build_object('label', 'UN_8', 'value', t.un8),
        json_build_object('label', 'UN_9', 'value', t.un9),
        json_build_object('label', 'unspecified', 'value', t.unspecified),
        json_build_object('label', 'multiple', 'value', t.multiple)
        
    )
    )
from
    t
{handle_c(c)};
"""