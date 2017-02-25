# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, DateTime, BigInteger, String, Float

from orm.models.base import Base

SCHEMA = {"schema": "paipaidai"}


class PaipaidaiBusinessInfo(Base):
    """
    ORM,one class in code is one table in database
    """
    __tablename__ = 'business_info'
    __table_args__ = SCHEMA

    id = Column(Integer, primary_key=True, autoincrement=True)
    userscount = Column(BigInteger)
    loanamount = Column(BigInteger)
    dealvolume = Column(BigInteger)
    crawl_date = Column(DateTime)


class PaipaidaiPaihuobao(Base):
    __tablename__ = 'paihuobao'
    __table_args__ = SCHEMA

    id = Column(Integer, primary_key=True, autoincrement=True)
    annualized_rate_of_return = Column(String)
    aucumulated_investment = Column(BigInteger)
    total_invest_users = Column(BigInteger)
    aucumulated_profit = Column(BigInteger)
    crawl_date = Column(DateTime)


class PaipaidaiRainbowInfo(Base):
    __tablename__ = 'rainbowinfo'
    __table_args__ = SCHEMA

    id = Column(Integer, primary_key=True, autoincrement=True)
    rainbow_invest_count = Column(BigInteger)
    rainbow_service_users = Column(BigInteger)
    rainbow_profit = Column(BigInteger)
    crawl_date = Column(DateTime)


class PaipaidaiYueyuezhang(Base):
    __tablename__ = 'yueyuezhang'
    __table_args__ = SCHEMA

    id = Column(Integer, primary_key=True, autoincrement=True)
    yueyuezhang_phase = Column(String)
    annualized_rate_of_return = Column(String)
    invest_term = Column(String)
    total_amount = Column(Float)
    remain_amount_cast = Column(Float)
    purchase_limit = Column(Float)
    aucumulated_investment = Column(Float)
    total_invest_users = Column(BigInteger)
    aucumulated_profit = Column(Float)
    crawl_date = Column(DateTime)


class PaipaidaiRainbowPlan(Base):
    __tablename__ = 'rainbowplan'
    __table_args__ = SCHEMA

    plan_id = Column(Integer, primary_key=True)
    annualized_rate_of_return = Column(String)
    invest_term = Column(String)
    total_amount = Column(Float)
    remain_amount_cast = Column(Float)
    purchase_limit = Column(Float)
    start_purchase_date = Column(String)
    income_date = Column(String)
    crawl_date = Column(DateTime)
    source_url = Column(String)


class PaipaidaiUserinfo(Base):
    __tablename__ = 'userinfo'
    __table_args__ = SCHEMA

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String)
    user_sex = Column(String)
    user_age = Column(String)
    borrow_credit = Column(Integer)
    loan_credit = Column(Integer)
    identity = Column(String)
    crawl_date = Column(DateTime)


class PaipaidaiLoanInfo(Base):
    __tablename__ = 'loaninfo'
    __table_args__ = SCHEMA

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String)
    successful_times = Column(Integer)
    failed_times = Column(Integer)
    credit_rank = Column(String)
    crawl_date = Column(DateTime)