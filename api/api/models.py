# coding: utf-8
from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Export(Base):
    __tablename__ = 'exports'

    id = Column(Integer, primary_key=True)
    country = Column(String(2))
    country_of_destination = Column(String(2))
    year = Column(Integer)
    amount = Column(Float(53))
    h1 = Column(Boolean)
    h3 = Column(Boolean)
    h4_1 = Column(Boolean)
    h4_2 = Column(Boolean)
    h4_3 = Column(Boolean)
    h5_1 = Column(Boolean)
    h5_2 = Column(Boolean)
    h6_1 = Column(Boolean)
    h6_2 = Column(Boolean)
    h8 = Column(Boolean)
    h10 = Column(Boolean)
    h11 = Column(Boolean)
    h12 = Column(Boolean)
    h13 = Column(Boolean)
    d1 = Column(Boolean)
    d2 = Column(Boolean)
    d3 = Column(Boolean)
    d4 = Column(Boolean)
    d5 = Column(Boolean)
    d6 = Column(Boolean)
    d7 = Column(Boolean)
    d8 = Column(Boolean)
    d9 = Column(Boolean)
    d10 = Column(Boolean)
    d11 = Column(Boolean)
    d12 = Column(Boolean)
    d13 = Column(Boolean)
    d14 = Column(Boolean)
    d15 = Column(Boolean)
    d16 = Column(Boolean)
    r1 = Column(Boolean)
    r2 = Column(Boolean)
    r3 = Column(Boolean)
    r4 = Column(Boolean)
    r5 = Column(Boolean)
    r6 = Column(Boolean)
    r7 = Column(Boolean)
    r8 = Column(Boolean)
    r9 = Column(Boolean)
    r10 = Column(Boolean)
    r11 = Column(Boolean)
    r12 = Column(Boolean)
    r13 = Column(Boolean)

   
