import sqlalchemy as sa
from sqlalchemy import orm
from datajongleur.neuro.pq_based import *

def map_pq_based(metadata):
  # Table specification
  moment_table = sa.Table(
      'dj_neuro_moments', metadata,
      sa.Column('moment_key', sa.Integer, primary_key=True),
      sa.Column('time', sa.Float),
      sa.Column('units', sa.String))

  period_table = sa.Table(
      'dj_neuro_periods', metadata,
      sa.Column('period_key', sa.Integer, primary_key=True),
      sa.Column('start', sa.Float),
      sa.Column('stop', sa.Float),
      sa.Column('units', sa.String)
      )
  # Mapping
  orm.mapper(MomentDTO, moment_table)
  orm.mapper(PeriodDTO, period_table)

def connect_db(db_name='sqlite:///test.sqlite', echo=True):
  """
  Examples for `db_name`:
  >>> db_name = "sqlite:///foo.db"
  >>> db_name = "sqlite:////absolut/path/foo.db"
  >>> db_name = "postgresql://hal08.g-node.pri/lehmann" # user + pwd: ~/.pgpass
  >>> db_name = "postgresql://user:pwd@hal08.g-node.pri/lehmann"
  """
  engine = sa.create_engine(db_name, echo=echo)
  connection = engine.connect()
  Session = orm.sessionmaker()
  Session.configure(bind=connection)
  session = Session()
  metadata = sa.MetaData(bind=connection)
  map_pq_based(metadata)
  return metadata, session, connection

if __name__ == '__main__':
  import random
  m,s,c = connect_db()
  m.create_all()
  b = MomentDTO(random.random(), 'ms')
  s.add(b)
  s.commit()
