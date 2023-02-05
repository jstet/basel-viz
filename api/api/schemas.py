from pydantic import BaseModel
from pydantic.schema import Optional, List
from datetime import datetime

class Properties(BaseModel):
    code: str

class Geometry_Point(BaseModel):
    type: "Point"
    coordinates: List[float]

class Geometry_Line(BaseModel):
    type: "LineString"
    coordinates: List[List[float]]


class Features_Line(BaseModel):
    type: "Feature"
    properties: Properties
    geometry: Geometry_Line

class Line(BaseModel):
    type: "FeatureCollection"
    features: List[Features_Line]

    class Config:
        orm_mode = True



    

    