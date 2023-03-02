def handle_s(s):
    if s is None:
        where = ""
    else:
        where = f"""
         where
        origin = '{s}' or destination = '{s}';
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
        return f"{l}_{type}" if l != "country" else f"{type}"
    else:
        return f"{table}.{l}_{type}" if l != "country" else f"{table}.{type}"


def handle_where(l, y, points, type, table=""):
    print(points)
    if y is None:
        if points:
            return ""
        else:
            return f"where {handle_name(l, 'code', 'c1')}  != {handle_name(l, 'code', 'c2')}"
    else:
        if points:
            return ""
        else:
            return f"and {handle_name(l, 'code', 'c1')}  != {handle_name(l, 'code', 'c2')}"


def handle_n(n, table=""):
    if n == True:
        pop = f"SUM({'' if table == '' else table + '.'}population)"
        return pop
    else:
        return 1


def handle_l(y, n, l, points, u, s=""):
    if l != 'country':
        return f""" 
        with t1 as (
select distinct
    {f"(SUM(un1)/{handle_n(n,'c1')}) as un1," if u == None or u=='1' else "0 as un1,"}
    {f"(SUM(un3)/{handle_n(n,'c1')}) as un3," if u == None or u=='3' else "0 as un3,"}
    {f"(SUM(un4_1)/{handle_n(n,'c1')}) as un4_1," if u == None or u=='4_1' else "0 as un4_1,"}
    {f"(SUM(un4_2)/{handle_n(n,'c1')}) as un4_2," if u == None or u=='4_2' else "0 as un4_2,"}
    {f"(SUM(un4_3)/{handle_n(n,'c1')}) as un4_3," if u == None or u=='4_3' else "0 as un4_3,"}
    {f"(SUM(un5_1)/{handle_n(n,'c1')}) as un5_1," if u == None or u=='5_1' else "0 as un5_1,"}
    {f"(SUM(un5_2)/{handle_n(n,'c1')}) as un5_2," if u == None or u=='5_2' else "0 as un5_2,"}
    {f"(SUM(un6_1)/{handle_n(n,'c1')}) as un6_1," if u == None or u=='6_1' else "0 as un6_1,"}
    {f"(SUM(un6_2)/{handle_n(n,'c1')}) as un6_2," if u == None or u=='6_2' else "0 as un6_2,"}
    {f"(SUM(un8)/{handle_n(n,'c1')}) as un8," if u == None or u=='8' else "0 as un8,"}
    {f"(SUM(un9)/{handle_n(n,'c1')}) as un9," if u == None or u=='9' else "0 as un9,"}
    {f"(SUM(unspecified)/{handle_n(n,'c1')}) as unspecified," if u == None or u=='unspecified' else "0 as unspecified,"}
    {f"(SUM(multiple)/{handle_n(n,'c1')}) as multiple," if u == None or u=='multiple' else "0 as multiple,"}
	{f"c1.{l}_code" if l!="country" else "c1.code"} as origin
    {f"" if points else ", " + handle_name(l,"code","c2") + " as destination" }
	
from
	exports as ex
	inner join countries as c1 on
	ex.origin =  c1.code
    {"" if points else "inner join countries as c2 on ex.destination = c2.code"}
{handle_y(y)}
{handle_where(l=l, y=y, points=points, table="c1", type="code")}

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
    {"" if points else "destination,"}
	(SUM(un1){"/(select population from countries where code = origin)" if n else ""}) as un1,
	(SUM(un3){"/(select population from countries where code = origin)" if n else ""}) as un3,
	(SUM(un4_1){"/(select population from countries where code = origin)" if n else ""}) as un4_1,
	(SUM(un4_2){"/(select population from countries where code = origin)" if n else ""}) as un4_2,
	(SUM(un4_3){"/(select population from countries where code = origin)" if n else ""}) as un4_3,
	(SUM(un5_1){"/(select population from countries where code = origin)" if n else ""}) as un5_1,
	(SUM(un5_2){"/(select population from countries where code = origin)" if n else ""}) as un5_2,
	(SUM(un6_1){"/(select population from countries where code = origin)" if n else ""}) as un6_1,
	(SUM(un6_2){"/(select population from countries where code = origin)" if n else ""}) as un6_2,
	(SUM(un8){"/(select population from countries where code = origin)" if n else ""}) as un8,
	(SUM(un9){"/(select population from countries where code = origin)" if n else ""}) as un9,
	(SUM(unspecified){"/(select population from countries where code = origin)" if n else ""}) as unspecified,
	(SUM(multiple){"/(select population from countries where code = origin)" if n else ""}) as multiple
from
       exports
{handle_y(y)}
group by
        origin
    {"" if points else ",destination"}
        )
        """


def unidirect_query(y, s, n, l, u):
    return f"""
    {handle_l( y=y, n=n, l=l, points = False, u=u)},

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
where (t1.origin, t1.destination) not in (select origin, destination from bidirect)	
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
            json_build_object('label', 'UN_5_2', 'value', unidirect.un5_2),
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


def bidirect_query(y, s, n, l, u):
    return f"""
    {handle_l(y=y, n=n, l=l, points=False, u=u)},
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
            json_build_object('label', 'UN_5_2', 'value', bidirect.un5_2),
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


def points_query(y, s, n, l, u):
    beginning = f"""
    
        with t1 as (
select distinct
        {f"(SUM(un1)/{handle_n(n,'c1')}) as un1," if u == None or u=='1' else "0 as un1,"}
        {f"(SUM(un3)/{handle_n(n,'c1')}) as un3," if u == None or u=='3' else "0 as un3,"}
        {f"(SUM(un4_1)/{handle_n(n,'c1')}) as un4_1," if u == None or u=='4_1' else "0 as un4_1,"}
        {f"(SUM(un4_2)/{handle_n(n,'c1')}) as un4_2," if u == None or u=='4_2' else "0 as un4_2,"}
        {f"(SUM(un4_3)/{handle_n(n,'c1')}) as un4_3," if u == None or u=='4_3' else "0 as un4_3,"}
        {f"(SUM(un5_1)/{handle_n(n,'c1')}) as un5_1," if u == None or u=='5_1' else "0 as un5_1,"}
        {f"(SUM(un5_2)/{handle_n(n,'c1')}) as un5_2," if u == None or u=='5_2' else "0 as un5_2,"}
        {f"(SUM(un6_1)/{handle_n(n,'c1')}) as un6_1," if u == None or u=='6_1' else "0 as un6_1,"}
        {f"(SUM(un6_2)/{handle_n(n,'c1')}) as un6_2," if u == None or u=='6_2' else "0 as un6_2,"}
        {f"(SUM(un8)/{handle_n(n,'c1')}) as un8," if u == None or u=='8' else "0 as un8,"}
        {f"(SUM(un9)/{handle_n(n,'c1')}) as un9," if u == None or u=='9' else "0 as un9,"}
        {f"(SUM(unspecified)/{handle_n(n,'c1')}) as unspecified," if u == None or u=='unspecified' else "0 as unspecified,"}
        {f"(SUM(multiple)/{handle_n(n,'c1')}) as multiple," if u == None or u=='multiple' else "0 as multiple,"}
        {handle_name(l, "code","c1")} as origin,
        SUM(un1) as abs_un1,
        SUM(un3) as abs_un3,
        SUM(un4_1) as abs_un4_1,
        SUM(un4_2) as abs_un4_2,
        SUM(un4_3) as abs_un4_3,
        SUM(un5_1) as abs_un5_1,
        SUM(un5_2) as abs_un5_2,
        SUM(un6_1) as abs_un6_1,
        SUM(un6_2) as abs_un6_2,
        SUM(un8) as abs_un8,
        SUM(un9) as abs_un9,
        SUM(unspecified) as abs_unspecified,
        SUM(multiple) as abs_multiple   
from
        exports as ex
        inner join countries as c1 on
        ex.origin =  c1.code
    
{handle_y(y)}

and ex.origin in (
select
	c2.code
from
	countries as c2
{f"where {handle_name(l, 'code')} = '{s}'" if s != None else ""})
        


group by
        {handle_name(l, "code","c1")}
    
        )

 """     
    imports = f""", imports as(
		select 
		{f"(SUM(un1)/{handle_n(n,'c1')}) as un1" if u == None or u=='1' else "0 as un1"},
        {f"(SUM(un3)/{handle_n(n,'c1')}) as un3" if u == None or u=='3' else "0 as un3"},
        {f"(SUM(un4_1)/{handle_n(n,'c1')}) as un4_1" if u == None or u=='4_1' else "0 as un4_1"},
        {f"(SUM(un4_2)/{handle_n(n,'c1')}) as un4_2" if u == None or u=='4_2' else "0 as un4_2"},
        {f"(SUM(un4_3)/{handle_n(n,'c1')}) as un4_3" if u == None or u=='4_3' else "0 as un4_3"},
        {f"(SUM(un5_1)/{handle_n(n,'c1')}) as un5_1" if u == None or u=='5_1' else "0 as un5_1"},
        {f"(SUM(un5_2)/{handle_n(n,'c1')}) as un5_2" if u == None or u=='5_2' else "0 as un5_2"},
        {f"(SUM(un6_1)/{handle_n(n,'c1')}) as un6_1" if u == None or u=='6_1' else "0 as un6_1"},
        {f"(SUM(un6_2)/{handle_n(n,'c1')}) as un6_2" if u == None or u=='6_2' else "0 as un6_2"},
        {f"(SUM(un8)/{handle_n(n,'c1')}) as un8" if u == None or u=='8' else "0 as un8"},
        {f"(SUM(un9)/{handle_n(n,'c1')}) as un9" if u == None or u=='9' else "0 as un9"},
        {f"(SUM(unspecified)/{handle_n(n,'c1')}) as unspecified" if u == None or u=='unspecified' else "0 as unspecified"},
        {f"(SUM(multiple)/{handle_n(n,'c1')}) as multiple" if u == None or u=='multiple' else "0 as multiple"},
		{handle_name(l, "code","c1")} as origin,
        SUM(un1) as abs_un1,
		SUM(un3) as abs_un3,
		SUM(un4_1) as abs_un4_1,
		SUM(un4_2) as abs_un4_2,
		SUM(un4_3) as abs_un4_3,
		SUM(un5_1) as abs_un5_1,
		SUM(un5_2) as abs_un5_2,
		SUM(un6_1) as abs_un6_1,
		SUM(un6_2) as abs_un6_2,
		SUM(un8) as abs_un8,
		SUM(un9) as abs_un9,
		SUM(unspecified) as abs_unspecified,
		SUM(multiple) as abs_multiple

		from
		exports as ex
		inner join countries as c1 on
		ex.origin =  c1.code 
	{handle_y(y)}
and ex.destination in (select c2.code
						from countries as c2
						{f"where {handle_name(l, 'code')} = '{s}'" if s != None else ""})
group by
        {handle_name(l, "code","c1")}
        )"""

    
    end= f""",final as (
	{f" select* from imports where imports.origin != '{s}' union" if s != None else ""}
	select
	*
	from
	t1)       

select
    json_build_object(
        'origin_code', final.origin,
        'un_classes', json_build_array(
        json_build_object('label', 'UN_1', 'value', final.un1),
        json_build_object('label', 'UN_3', 'value', final.un3),
        json_build_object('label', 'UN_4_1', 'value', final.un4_1),
        json_build_object('label', 'UN_4_2', 'value', final.un4_2),
        json_build_object('label', 'UN_4_3', 'value', final.un4_3),
        json_build_object('label', 'UN_5_1', 'value', final.un5_1),
        json_build_object('label', 'UN_5_2', 'value', final.un5_2),
        json_build_object('label', 'UN_6_1', 'value', final.un6_1),
        json_build_object('label', 'UN_6_2', 'value', final.un6_2),
        json_build_object('label', 'UN_8', 'value', final.un8),
        json_build_object('label', 'UN_9', 'value', final.un9),
        json_build_object('label', 'unspecified', 'value', final.unspecified),
        json_build_object('label', 'multiple', 'value', final.multiple)
        ),
        'abs_un_classes', json_build_array(
        json_build_object('label', 'UN_1', 'value', final.abs_un1),
        json_build_object('label', 'UN_3', 'value', final.abs_un3),
        json_build_object('label', 'UN_4_1', 'value', final.abs_un4_1),
        json_build_object('label', 'UN_4_2', 'value', final.abs_un4_2),
        json_build_object('label', 'UN_4_3', 'value', final.abs_un4_3),
        json_build_object('label', 'UN_5_1', 'value', final.abs_un5_1),
        json_build_object('label', 'UN_5_2', 'value', final.abs_un5_2),
        json_build_object('label', 'UN_6_1', 'value', final.abs_un6_1),
        json_build_object('label', 'UN_6_2', 'value', final.abs_un6_2),
        json_build_object('label', 'UN_8', 'value', final.abs_un8),
        json_build_object('label', 'UN_9', 'value', final.abs_un9),
        json_build_object('label', 'unspecified', 'value', final.abs_unspecified),
        json_build_object('label', 'multiple', 'value', final.abs_multiple)
    )
    )
from
    final
"""

    if s is None:
        return beginning + end
    else:
        return beginning + imports + end



def countries_query():
    return f"""
    select json_build_object(
        code,  json_build_object(
            'name', name, 'coordinates', json_build_array(lat, lon)
            )
            )
    from countries
    """


def coords_query(l, d):
    return f"""
    select json_build_object(
        {f"{l}_code" if l!="country" else "code"},  json_build_object(
            'name', {f"{l}_name" if l!="country" else "name"}, 'coordinates', json_build_array({f"{l}_lat" if l!="country" else "lat"}, {f"{l}_lon" if l!="country" else "lon"})
            )
            )
    from countries
    {"where destination_only = False" if d else ""}
    order by {handle_name(l, 'name')}
    """


def handle_y2(y):
    if y is None:
        where = ""
    else:
        where = f""" year between {y[0]} and {y[1]}"""
    return where


def no_exports_query(l, y, s):
    return f"""
    with noExports as (
    select distinct {handle_name(l, 'code', 'countries')}, {handle_name(l, 'name', 'countries')}, {handle_name(l, 'lat', 'countries')}, {handle_name(l, 'lon', 'countries')}
    from exports join countries on exports.destination=countries.code
    {"" if y==None else "where " + handle_y2(y)}

    {"{temp}".format(temp=("where" if y is None and s is not None else "and" if s is not None else ""))} 
    {f"exports.origin in (select c2.code from countries as c2 where '{s}' = {handle_name(l, 'code', 'c2')})" if s != None else ""}
    except
	
    select distinct {handle_name(l, 'code')}, {handle_name(l, 'name')}, {handle_name(l, 'lat')}, {handle_name(l, 'lon')}
    from countries as c join exports as e on e.origin=c.code
    {"{temp}".format(temp=("where" if y is None and s is not None else "and" if s is not None else ""))} 
    {f"e.destination in (select c2.code from countries as c2 where '{s}' = {handle_name(l, 'code', 'c2')})" if s != None else ""}
    )
    select json_build_object(
        'origin_code', {handle_name(l, 'code')})
    from noExports
    order by {handle_name(l, 'name')}
    """
