import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects.postgresql import ARRAY as PGArray
from datajongleur.neuro.pq_based import *

PREFIX = 'dj_neuro_'
SCHEMANAME = 'sandkasten'
DEFAULT_CONNECTION = "postgresql://localhost/rautiation"

def map_pq_based(metadata, schemaname=SCHEMANAME):
  # Table specification
  moment_table = sa.Table(
      PREFIX + 'moments', metadata,
      sa.Column('moment_key', sa.Integer, primary_key=True),
      sa.Column('time', sa.Float),
      sa.Column('units', sa.String),
      schema=schemaname)

  period_table = sa.Table(
      PREFIX + 'periods', metadata,
      sa.Column('period_key', sa.Integer, primary_key=True),
      sa.Column('start', sa.Float),
      sa.Column('stop', sa.Float),
      sa.Column('units', sa.String),
      schema = schemaname)

  sampled_time_series_table = sa.Table(
      PREFIX + 'sampled_time_series', metadata,
      sa.Column('sampled_time_series_key', sa.Integer, primary_key=True),
      sa.Column('signal', PGArray(sa.Float)),
      sa.Column('signal_units', sa.String),
      sa.Column('signal_base', PGArray(sa.Float)),
      sa.Column('signal_base_units', sa.String),
      schema = schemaname)

  spike_times_table = sa.Table(
      PREFIX + 'spike_times', metadata,
      sa.Column('spiketimes_key', sa.Integer, primary_key=True),
      sa.Column('spiketimes', PGArray(sa.Float)),
      sa.Column('spiketimes_units', sa.String),
      schema = schemaname)

  regularly_sampled_time_series_table = sa.Table(
      PREFIX + 'regularly_sampled_time_series', metadata,
      sa.Column('regularly_sampled_time_series_key',
        sa.Integer, primary_key=True),
      sa.Column('sampled_signal', PGArray(sa.Float)),
      sa.Column('sampled_signal_units', sa.String),
      sa.Column('start', sa.Float),
      sa.Column('stop', sa.Float),
      sa.Column('time_units', sa.String),
      schema = schemaname)

  binned_spikes_table = sa.Table(
      PREFIX + 'binned_spikes', metadata,
      sa.Column('binned_spikes_key', sa.Integer, primary_key=True),
      sa.Column('sampled_signal', PGArray(sa.Integer)),
      sa.Column('start', sa.Float),
      sa.Column('stop', sa.Float),
      sa.Column('time_units', sa.String),
      schema = schemaname)

  # Mapping
  orm.mapper(MomentDTO, moment_table)
  orm.mapper(PeriodDTO, period_table)
  orm.mapper(SampledTimeSeriesDTO, sampled_time_series_table)
  orm.mapper(SpikeTimesDTO, spike_times_table)
  orm.mapper(
      RegularlySampledTimeSeriesDTO,
      regularly_sampled_time_series_table)
  orm.mapper(BinnedSpikesDTO, binned_spikes_table)

def connect_db(db_name=DEFAULT_CONNECTION, echo=True):
  """
  Examples for `db_name`:
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
  # MomentDTO
  m = MomentDTO(random.random(), 'ms')
  s.add(m)
  s.commit()
  # PeriodDTO
  p = PeriodDTO(random.random(), 1.1, 'ns')
  s.add(p)
  s.commit()
  # SampledTimeSeriesDTO
  sts = SampledTimeSeriesDTO([1,2,3], 'mV', [1,4,7], 's')
  s.add(sts)
  s.commit()
  # SpikeTimesDTO
  spiketimes = SpikeTimesDTO([1.3, 1.9, 2.5], "ms")
  s.add(spiketimes)
  s.commit()
  # RegularlySampledTimeSeriesDTO
  rsts = RegularlySampledTimeSeriesDTO([1,2,3],"mV", 1, 5, "s")
  s.add(rsts)
  s.commit()
  # BinnedSpikesDTO
  bs = BinnedSpikesDTO([5,6,2], 1.3, 5.9, "ms")
  s.add(bs)
  s.commit()
  
