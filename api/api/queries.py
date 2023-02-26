def handle_s(s):
    if s is None:
        where = ""
    else:
        where = f"""
         where
        origin = '{s}';
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

def handle_name(l, type, table=""):
    if table == "":
        print({f"{l}_{type}" if l!="country" else "{type}"})
        return f"{l}_{type}" if l!="country" else "{type}"
    else:
        print({f"{table}.{l}_{type}" if l!="country" else "{table}.{type}"})
        return f"{table}.{l}_{type}" if l!="country" else "{table}.{type}"


def handle_n(n):
    if n == True:
        pop = f"SUM(c1.population)"
        return pop
    else:
        return 1

def handle_l(y, n, l, points):
    if l != 'country':
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
	{f"c1.{l}_code" if l!="country" else "c1.code"} as origin
    {f"" if points else ", " + handle_name(l,"code","c2") + " as destination" }
	
from
	exports as ex
	inner join countries as c1 on
	ex.origin =  c1.code
    {"" if points else "inner join countries as c2 on ex.destination = c2.code"}
{handle_y(y)}
{"" if points else "and " +  handle_name(l, "code", "c1")  + "!=" + handle_name(l, "code", "c2")}
group by
	{handle_name(l, "code", "c1")}
    {"" if points else ", " + handle_name(l, "code", "c2")}
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


def unidirect_query(y, s, n, l):
    return f"""
    {handle_l( y=y, n=n, l=l, points = False)},

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
        
    {handle_s(s)};
    """


def bidirect_query(y, s, n, l):
    return f"""
    {handle_l(y=y, n=n, l=l, points=False)},
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

    {handle_s(s)};
    """


def points_query(y, s, n, l ):
    print(y)
    return f"""
    
{handle_l(y=y, n=n, l=l, points=True)}

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
{handle_s(s)};
"""


def countries_query():
    return f"""
    select json_build_object(
        code,  json_build_object(
            'name', name, 'coordinates', json_build_array(lat, lon)
            )
            )
    from countries
    """

def coords_query(l):
    return f"""
    select json_build_object(
        {f"{l}_code" if l!="country" else "code"},  json_build_object(
            'name', {f"{l}_name" if l!="country" else "name"}, 'coordinates', json_build_array({f"{l}_lat" if l!="country" else "lat"}, {f"{l}_lon" if l!="country" else "lon"})
            )
            )
    from countries
    """

def handle_y2(y):
    if y is None:
        where = ""
    else:
        where = f""" year between {y[0]} and {y[1]}"""
    return where

def noExports_query(l, y):
    return f"""
    with noExports as (
    
    select distinct {f"{l}_code" if l!="countries" else "code"}, {f"{l}_name" if l!="countries" else "name"}, {f"{l}_lat" if l!="countries" else "lat"}, {f"{l}_lon" if l!="countries" else "lon"}
    from

    (select distinct {f"{l}_code" if l!="countries" else "code"}, {f"{l}_name" if l!="countries" else "name"}, {f"{l}_lat" if l!="countries" else "lat"}, {f"{l}_lon" if l!="countries" else "lon"}
    from countries join exports on exports.destination=countries.code

    union
    
    select distinct {f"{l}_code" if l!="countries" else "code"}, {f"{l}_name" if l!="countries" else "name"}, {f"{l}_lat" if l!="countries" else "lat"}, {f"{l}_lon" if l!="countries" else "lon"}
    from countries join exports on exports.origin=countries.code) as total

    except
	
    select distinct {f"{l}_code" if l!="countries" else "code"}, {f"{l}_name" if l!="countries" else "name"}, {f"{l}_lat" if l!="countries" else "lat"}, {f"{l}_lon" if l!="countries" else "lon"}
    from exports as e2 join countries as c on  e2.origin=c.code
    {"" if y==None else "where" + handle_y2(y)}
    )                                

    select json_build_object(
        {"code" if l=='countries' else "sub_region_code" if l=='sub_regions' else "region_code"},  json_build_object(
            'name', {handle_name(l, 'code') if l!="countries" else "code"}, 'coordinates', json_build_array({handle_name(l, 'lat') if l!="countries" else "lat"}, {handle_name(l, 'lon') if l!="countries" else "lon"})
            )
            )
    from noExports
    """