from datajongleur.models import Base, declarative_base
import sqlalchemy as sa
import sqlalchemy.orm as orm
import datetime as dt
from sqlalchemy import exc
from datajongleur.neuro.pq_based import *

PREFIX = 'dj_neuro_'

class NumpyType (sa.types.TypeDecorator):
  import zlib, bz2
  impl = sa.types.LargeBinary

  def process_bind_param(self, value, dialect):
    return zlib.compress(value.dumps(), 9)

  def process_result_value(self, value, dialect):
    return np.loads(zlib.decompress(value))

def map_pq_beanbags(metadata, schemaname=SCHEMANAME):
  # Table specification
  time_point_table = sa.Table(
      PREFIX + 'time_points', metadata,
      sa.Column('time_point_key', sa.BigInteger, primary_key=True),
      sa.Column('time', sa.Float),
      sa.Column('units', sa.String),
      schema=schemaname)

  period_table = sa.Table(
      PREFIX + 'periods', metadata,
      sa.Column('period_key', sa.BigInteger, primary_key=True),
      sa.Column('start', sa.Float),
      sa.Column('stop', sa.Float),
      sa.Column('units', sa.String),
      )

  sampled_time_series_table = sa.Table(
      PREFIX + 'sampled_time_series', metadata,
      sa.Column('sampled_time_series_key', sa.BigInteger, primary_key=True),
      sa.Column('signal', NumpyType),
      sa.Column('signal_units', sa.String),
      sa.Column('signal_base', NumpyType),
      sa.Column('signal_base_units', sa.String),
      )

  spike_times_table = sa.Table(
      PREFIX + 'spike_times', metadata,
      sa.Column('spike_times_key', sa.BigInteger, primary_key=True),
      sa.Column('spike_times', NumpyType),
      sa.Column('spike_times_units', sa.String),
      )

  regularly_sampled_time_series_table = sa.Table(
      PREFIX + 'regularly_sampled_time_series', metadata,
      sa.Column('regularly_sampled_time_series_key',
        sa.BigInteger, primary_key=True),
      sa.Column('sampled_signal', NumpyType),
      sa.Column('sampled_signal_units', sa.String),
      sa.Column('start', sa.Float),
      sa.Column('stop', sa.Float),
      sa.Column('time_units', sa.String),
      )

  binned_spikes_table = sa.Table(
      PREFIX + 'binned_spikes', metadata,
      sa.Column('binned_spikes_key', sa.BigInteger, primary_key=True),
      sa.Column('sampled_signal', PGArray(sa.Integer)),
      sa.Column('start', sa.Float),
      sa.Column('stop', sa.Float),
      sa.Column('time_units', sa.String),
      )

  # Mapping
  orm.mapper(TimePointDTO, time_point_table)
  orm.mapper(PeriodDTO, period_table)
  orm.mapper(SampledTimeSeriesDTO, sampled_time_series_table)
  orm.mapper(SpikeTimesDTO, spike_times_table)
  orm.mapper(
      RegularlySampledTimeSeriesDTO,
      regularly_sampled_time_series_table)
  orm.mapper(BinnedSpikesDTO, binned_spikes_table)

  # Create non existing tables
  metadata.create_all()

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
  return metadata, session, connection

####################
# Container-Jongleur
####################

class CJ(object):
  def __init__(self, db_name=DEFAULT_CONNECTION, echo=True):
    m,s,c = connect_db(db_name, echo)
    try:
      map_pq_beanbags(m)
    except exc.SQLAlchemyError, e:
      print "Mapping problem: %s" %(e[0])
    try:
      map_container(m)
    except exc.SQLAlchemyError, e:
      print "Mapping problem (container): %s" %(e[0])
    self.metadata = m
    self.session = s
    self.connection = c

  def getContainerDict(self):
    list_of_containers = self.getContainerList()
    dict_of_containers = {}
    for container in list_of_containers:
      print container.name
      dict_of_containers[container.name] = container
    return dict_of_containers

  def getContainerList(self):
    list_of_containers = self.session.query(Container).all()
    return list_of_containers

  def addContainer(self, container):
    assert isinstance(container, Container)
    self.session.add(container)
    self.session.commit()


class Container(object):
  def __init__(self, name):
    self.name = name

  def addTimePoint(self):
    pass

  def __repr__(self):
    return "Container(%r)" %(self.name)

def map_container(metadata, schemaname=SCHEMANAME):
  container_table = sa.Table(
      PREFIX + "container", metadata,
      sa.Column('name', sa.TEXT, primary_key=True),
      sa.Column('creation_time', sa.DateTime, default=dt.datetime.now()),
      # PR: now() is not implemented on the level of SQL
      )

  container_time_point_map_table = sa.Table(
      PREFIX + "container_time_point_map", metadata,
      sa.Column('time_point_key',
        sa.BigInteger,
        sa.ForeignKey(schemaname + "." + PREFIX + 'time_points.time_point_key')),
      sa.Column('name', 
        sa.TEXT,
        sa.ForeignKey(schemaname + "." + PREFIX + 'container.name')),
      sa.PrimaryKeyConstraint('time_point_key', 'name'),
      
      )

  container_period_map_table = sa.Table(
      PREFIX + 'container_period_map', metadata,
      sa.Column('period_key',
        sa.BigInteger,
        sa.ForeignKey(schemaname + '.' + PREFIX + 'periods.period_key')),
      sa.Column('name', 
        sa.TEXT,
        sa.ForeignKey(schemaname + "." + PREFIX + 'container.name')),
      sa.PrimaryKeyConstraint('period_key', 'name'),
      
      )

  container_sampled_time_series_map_table = sa.Table(
      PREFIX + "container_sampled_time_series_map", metadata,
      sa.Column('sampled_time_series_key',
        sa.BigInteger,
        sa.ForeignKey(
          schemaname + "." + PREFIX + 'sampled_time_series.sampled_time_series_key')),
      sa.Column('name', 
        sa.TEXT,
        sa.ForeignKey(schemaname + "." + PREFIX + 'container.name')),
      sa.PrimaryKeyConstraint('sampled_time_series_key', 'name'),
      
      )

  container_spike_times_map_table = sa.Table(
      PREFIX + 'container_spike_times_map', metadata,
      sa.Column('spike_times_key',
        sa.BigInteger,
        sa.ForeignKey(schemaname + '.' + PREFIX +\
            'spike_times.spike_times_key')),
      sa.Column('name', 
        sa.TEXT,
        sa.ForeignKey(schemaname + "." + PREFIX + 'container.name')),
      sa.PrimaryKeyConstraint('spike_times_key', 'name'),
      
      )

  container_regularly_sampled_time_series_map_table = sa.Table(
      PREFIX + 'container_regularly_sampled_time_series_map', metadata,
      sa.Column('regularly_sampled_time_series_key',
        sa.BigInteger,
        sa.ForeignKey(schemaname + '.' + PREFIX +\
          'regularly_sampled_time_series.regularly_sampled_time_series_key')),
      sa.Column('name', 
        sa.TEXT,
        sa.ForeignKey(schemaname + "." + PREFIX + 'container.name')),
      sa.PrimaryKeyConstraint('regularly_sampled_time_series_key', 'name'),
      
      )

  container_binned_spikes_map_table = sa.Table(
      PREFIX + 'container_binned_spikes_map', metadata,
      sa.Column('binned_spikes_key',
        sa.BigInteger,
        sa.ForeignKey(schemaname + '.' + PREFIX +\
            'binned_spikes.binned_spikes_key')),
      sa.Column('name', 
        sa.TEXT,
        sa.ForeignKey(schemaname + "." + PREFIX + 'container.name')),
      sa.PrimaryKeyConstraint('binned_spikes_key', 'name'),
      
      )

  orm.mapper(Container, container_table, properties=dict(
    _time_points=orm.relation(
        TimePointDTO,
        secondary=container_time_point_map_table,
        backref='_containers'),
    _periods=orm.relation(
        PeriodDTO,
        secondary=container_period_map_table,
        backref='_containers'),
    _sampled_time_series=orm.relation(
        SampledTimeSeriesDTO,
        secondary=container_sampled_time_series_map_table,
        backref='_containers'),
    _spike_times=orm.relation(
        SpikeTimesDTO,
        secondary=container_spike_times_map_table,
        backref='_containers'),
    _regularly_sampled_time_series=orm.relation(
        RegularlySampledTimeSeriesDTO,
        secondary=container_regularly_sampled_time_series_map_table,
        backref='_containers'),
    _binned_spikes=orm.relation(
        BinnedSpikesDTO,
        secondary=container_binned_spikes_map_table,
        backref='_containers'),
    ))
  metadata.create_all()

################################



if __name__ == '__main__':
  import random
  cj = CJ()
  d = cj.getContainerDict()
  l = cj.getContainerList()
  if False:
    # TimePointDTO
    m = TimePointDTO(random.random(), 'ms')
    cj.session.add(m)
    cj.session.commit()
    # PeriodDTO
    p = PeriodDTO(random.random(), 1.1, 'ns')
    cj.session.add(p)
    cj.session.commit()
    # SampledTimeSeriesDTO
    sts = SampledTimeSeriesDTO([1,2,3], 'mV', [1,4,7], 's')
    cj.session.add(sts)
    cj.session.commit()
    # SpikeTimesDTO
    spiketimes = SpikeTimesDTO([1.3, 1.9, 2.5], "ms")
    cj.session.add(spiketimes)
    cj.session.commit()
    # RegularlySampledTimeSeriesDTO
    rsts = RegularlySampledTimeSeriesDTO([1,2,3],"mV", 1, 5, "s")
    cj.session.add(rsts)
    cj.session.commit()
    # BinnedSpikesDTO
    bs = BinnedSpikesDTO([5,6,2], 1.3, 5.9, "ms")
    cj.session.add(bs)
    cj.session.commit()
    
