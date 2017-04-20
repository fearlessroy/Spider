# -*- coding:utf-8 -*-
from sqlalchemy import Column, String, Integer, DateTime
from orm.models.base import Base

SCHEMA = {"schema": "headline"}


class qiushibaike(Base):
    """
    ORM,one class in code is one table in database
    """
    __tablename__ = 'news'
    __table_args__ = SCHEMA

    id = Column(Integer, primary_key=True, info={"identity": (0, 1)})
    title = Column(String(128))
    link = Column(String(256))
    image = Column(String(256))
    like_count = Column(Integer)
    comment_count = Column(Integer)
    created_date = Column(DateTime)
    user_id = Column(Integer)
