from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import engine_from_config

from datajongleur.utils.config import ConfigJongleur
from datajongleur.utils.dto import BBConverter

Base = declarative_base()
DBSession = scoped_session(sessionmaker())
cj = ConfigJongleur()
bbc = BBConverter()

def initialize_sql(engine):
  DBSession.configure(bind=engine)
  Base.metadata.bind = engine
  Base.metadata.create_all(engine)

def get_engine():
  return engine_from_config(cj.config, 'sqlalchemy.')

def get_session():
  engine = get_engine()
  initialize_sql(engine)
  session = DBSession()
  return session
