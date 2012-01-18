from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import engine_from_config

from datajongleur.utils.config import LoadConfig

DBSession = scoped_session(sessionmaker())
#session = DBSession ()
Base = declarative_base()

#from beanbags.models import initialize_sql as initialize_beanbags
#from neuro.models import initialize_sql as initialize_neuro
#from neuro.neo.models import initialize_sql as initialize_neo
from beanbags.models import *
from addendum.models import *
from ext.neuro.models import *
from ext.neuro.neo.models import *

config = LoadConfig('db_setup.ini')
engine = engine_from_config(config, 'sqlalchemy.')

def initialize_sql(engine):
  DBSession.configure(bind=engine)
  Base.metadata.bind = engine
  Base.metadata.create_all(engine)

initialize_sql(engine)

session = DBSession ()
