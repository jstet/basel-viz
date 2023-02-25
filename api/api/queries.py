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


def handle_n(n):
    if n == True:
        pop = f"SUM(c1.population)"
        return pop
    else:
        return 1

def handle_l(y, n, c, l, points):
    if l != 0:
        return f""" 
        with t1 as (
select
	(SUM(un1)/{handle_n(n)}) as un1,
	(SUM(un3)/{handle_n(n)}) as un3,
	(SUM(un4_1)/{handle_n(n)}) as un4_1,
	(SUM(un4_2)/{handle_n(n)}) as un4_2,
	(SUM(un4_3)/{handle_n(n)}) as un4_3,
	(SUM(un5_1)/{handle_n(n)}) as un5_1,
	(SUM(un5_2)/{handle_n(n)}) as un5_2,
	(SUM(un6_1)/{handle_n(n)}) as un6_1,
	(SUM(un6_2)/{handle_n(n)}) as un6_2,
	(SUM(un8)/{handle_n(n)}) as un8,
	(SUM(un9)/{handle_n(n)}) as un9,
	(SUM(unspecified)/{handle_n(n)}) as unspecified,
	(SUM(multiple)/{handle_n(n)}) as multiple,
	c1.label_{l} as origin
     {"" if points else ", c2.label_{l} as destination"}
	
from
	exports as ex
	inner join countries as c1 on
	ex.origin = c1.country 
    {"" if points else "inner join countries as c2 on ex.destination = c2.country"}
{handle_y(y)}
{"" if points else "and c1.label_{l} != c2.label_{l}"}
group by
	c1.label_{l}
    {"" if points else ", c2.label_{l}"}
        )
            """
    else:
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
        )
        """


def unidirect_query(y, c, n, l):
    return f"""
    {handle_l( c=c, y=y, n=n, l=l, points = False)},

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


def bidirect_query(y, c, n, l):
    return f"""
    {handle_l( c=c, y=y, n=n, l=l, points=False)},
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


def points_query(y, c, n, l ):
    return f"""
{handle_l(c=c, y=y, n=n, l=l, points=True)}

select
    json_build_object(
        'origin_code', t1.origin,
        'un_classes', json_build_array(
        json_build_object('label', 'UN_1', 'value', t1.un1),
        json_build_object('label', 'UN_3', 'value', t1.un3),
        json_build_object('label', 'UN_4_1', 'value', t1.un4_1),
        json_build_object('label', 'UN_4_2', 'value', t1.un4_2),
        json_build_object('label', 'UN_4_3', 'value', t1.un4_3),
        json_build_object('label', 'UN_5_1', 'value', t1.un5_1),
        json_build_object('label', 'UN_6_1', 'value', t1.un6_1),
        json_build_object('label', 'UN_6_2', 'value', t1.un6_2),
        json_build_object('label', 'UN_8', 'value', t1.un8),
        json_build_object('label', 'UN_9', 'value', t1.un9),
        json_build_object('label', 'unspecified', 'value', t1.unspecified),
        json_build_object('label', 'multiple', 'value', t1.multiple)
        
    )
    )
from
    t1
{handle_c(c)};
"""


def countries_query():
    return f"""
    select json_build_object(
        country,  json_build_object(
            'name', name, 'coordinates', json_build_array(lat_0, lon_0)
            )
            )
    from countries
    """

def coords_query(l):
    return f"""
    select json_build_object(
        country,  json_build_object(
            'name', {"name" if l==0 else f"label_{l}"}, 'coordinates', json_build_array(lat_{l}, lon_{l})
            )
            )
    from countries
    """
