# coding: utf-8
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Coord(Base):
    __tablename__ = 'coords'

    country = Column(String(2), primary_key=True)
    lat = Column(Float(53))
    lon = Column(Float(53))


class Export(Base):
    __tablename__ = 'exports'

    id = Column(Integer, primary_key=True)
    origin = Column(String(2))
    destination = Column(String(2))
    year = Column(Integer)
    un1 = Column(Float(53))
    un3 = Column(Float(53))
    un4_1 = Column(Float(53))
    un4_2 = Column(Float(53))
    un4_3 = Column(Float(53))
    un5_1 = Column(Float(53))
    un5_2 = Column(Float(53))
    un6_1 = Column(Float(53))
    un6_2 = Column(Float(53))
    un8 = Column(Float(53))
    un9 = Column(Float(53))
    unspecified = Column(Float(53))
    multiple = Column(Float(53))
