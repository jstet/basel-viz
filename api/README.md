## Set up
1. Create new environment 
2. Activate environment
3. Install requirements

## Starting API
1. Start DB
```
docker compose -f database.yml down --volumes
docker compose -f database.yml  up --build --force-recreate
```
2. Start API (while in api/api folder)
```
uvicorn main:app --reload
```

## Refreshing models
With an activated environment and while in the api subfolder:
```
python create_models.py
```

## Query Dump
```
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
	json_build_object(
    'type',       'Feature',
    'id',         temp_table1.id,
    'properties', json_build_object(
    	'origin_code', temp_table1.origin,
    	'destination_code', temp_table1.destination,
        'un_classes', json_build_array(
         json_build_array('label', 'UN_1', 'value', temp_table1.un1),
         json_build_array('label', 'UN_3', 'value', temp_table1.un3),
         json_build_array('label', 'UN_4_1', 'value', temp_table1.un1),
         json_build_array('label', 'UN_4_2', 'value', temp_table1.un1),
         json_build_array('label', 'UN_4_3', 'value', temp_table1.un1),
         json_build_array('label', 'UN_5_1', 'value', temp_table1.un1),
         json_build_array('label', 'UN_6_1', 'value', temp_table1.un1),
         json_build_array('label', 'UN_6_2', 'value', temp_table1.un1),
         json_build_array('label', 'UN_8', 'value', temp_table1.un1),
         json_build_array('label', 'UN_9', 'value', temp_table1.un1),
          json_build_array('label', 'unspecified', 'value', temp_table1.unspecified),
           json_build_array('label', 'multiple', 'value', temp_table1.multiple)
       
     )
 ))
from
	temp_table2
inner join temp_table1 on
	temp_table2.id = temp_table1.id
where temp_table1.origin = 'de';
```