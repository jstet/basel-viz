# coding: utf-8
from sqlalchemy import Boolean, Column, Float, Integer, String
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
    amount = Column(Float(53))
    un1 = Column(Boolean)
    un3 = Column(Boolean)
    un4_1 = Column(Boolean)
    un4_2 = Column(Boolean)
    un4_3 = Column(Boolean)
    un5_1 = Column(Boolean)
    un5_2 = Column(Boolean)
    un6_1 = Column(Boolean)
    un6_2 = Column(Boolean)
    un8 = Column(Boolean)
    un9 = Column(Boolean)
