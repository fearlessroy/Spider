# -*- coding:utf-8 -*-
from sqlalchemy import Column, String, Integer
from orm.models.base import Base

SCHEMA = {"schema": "scrapy-spider"}


class ZhuanzibanCinema(Base):
    """
    ORM,one class in code is one table in database
    """
    __tablename__ = 'zhuanziban_cinema'
    __table_args__ = SCHEMA

    id = Column(Integer, primary_key=True, info={"identity": (0, 1)})
    cinema_company = Column(String(50))
    daily_box_office = Column(Integer)
    action_cutting = Column(Integer)
    daily_viewers = Column(Integer)
    counter_sales = Column(Integer)
    counter_sales_percent = Column(String(10))
    online_sales = Column(Integer)
    online_sales_percent = Column(String(10))
    date = Column(String(20))
