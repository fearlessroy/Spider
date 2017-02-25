# -*- coding:utf-8 -*-
from sqlalchemy import Column, String, BigInteger, DateTime, Integer, Float

from orm.models.base import Base

SCHEMA = {"schema": "tmall"}


class TmallProductInfo(Base):
    __tablename__ = 'product_info'
    __table_args__ = SCHEMA

    sku_id = Column(BigInteger,primary_key=True)
    title = Column(String(300))
    shop_id = Column(BigInteger)
    shop_name = Column(String(300))
    detail_url = Column(String(300))
    location = Column(String(30))
    seller_loc = Column(String(30))
    crawl_date = Column(DateTime)
    process_date = Column(DateTime)

    keys = ['sku_id', 'title', 'shop_id', 'shop_name', 'detail_url', 'location', 'seller_loc', 'crawl_date',
            'process_date']


class TmallSalesInfo(Base):
    __tablename__ = 'sales_info'
    __table_args__ = SCHEMA

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sku_id = Column(BigInteger)
    title = Column(String(300))
    price = Column(Float)
    original_price = Column(Float)
    sold = Column(BigInteger)
    comment_num = Column(BigInteger)
    category = Column(BigInteger)
    api_url = Column(String(300))
    crawl_date = Column(DateTime)
    process_date = Column(DateTime)

    keys = ['sku_id', 'title', 'price', 'original_price', 'sold', 'comment_num', 'category', 'api_url', 'crawl_date',
            'process_date']
