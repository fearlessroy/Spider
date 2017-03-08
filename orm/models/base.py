from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()  # orm base class
engine = create_engine('mysql+mysqlconnector://root:111@localhost:3306/scrapy-spider',
                       echo=True)  # init data base connrction
# create DBSession
DBSession = sessionmaker(bind=engine)
