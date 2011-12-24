import sqlalchemy as sa
import numpy as np
import sqlalchemy.orm as orm
from datajongleur import Base, DBSession
import uuid
from datajongleur.utils.sa import NumpyType, GUID
from datajongleur.utils.sa import passKeyDTO, addInfoQuantityDBAccess

PREFIX = 'dj_neuro_'

class DTOTimePoint(Base):
  __tablename__ =  PREFIX + 'time_points'

  key =  sa.Column('key', sa.Integer, primary_key=True)
  uuid = sa.Column('uuid', GUID, unique=True,
      default=uuid.uuid4)
  amount = sa.Column('amount', sa.Float)
  units = sa.Column('units', sa.String)

  def __init__(self, amount, units, **kwargs):
    self.amount = amount
    self.units = units

  def getDict(self):
    return {
        'amount': self.amount,
        'units': self.units}

  def getJSON(self):
    return json.dumps(self.getDict())

  def checksum_json(self):
    return checksum_json(self)

  def getXML(self):
    from datajongleur.tools.xml_jongleur import dict2xml
    xml = dict2xml(d)
    xml.display()
    return xml

  def __repr__(self):
    return "%s(%s, %r)" %(
        self.__class__.__name__,
        self.amount,
        self.units)


class DTOPeriod(Base):
  __tablename__ = PREFIX + 'periods'
  
  key = sa.Column('key', sa.Integer, primary_key=True)
  uuid = sa.Column('uuid', GUID, unique=True,
      default=uuid.uuid4)
  start = sa.Column('start', sa.Float)
  stop = sa.Column('stop', sa.Float)
  units = sa.Column('units', sa.String)

  def __init__(self, amount, units, **kwargs):
    try:
      self.start = amount[0]
      self.stop = amount[1]
    except IndexError, e:
      print e
      self.start = amount
      self.stop = amount
    self.units = units

  def getJSON(self):
    return json.dumps({
      'start': self.start,
      'stop': self.stop,
      'units': self.units})

  def checksum_json(self):
    return checksum_json(self)

  def __repr__(self):
    return "%s(start=%s, stop=%s, units=%r)" %(
        self.__class__.__name__,
        self.start,
        self.stop,
        self.units)


class DTOSampledTimeSeries(Base):
  __tablename__ = PREFIX + 'sampled_time_series'
  key = sa.Column(
      'key',
      sa.Integer,
      primary_key=True)
  uuid = sa.Column('uuid', GUID, unique=True,
      default=uuid.uuid4)
  amount = sa.Column('amount', NumpyType)
  units = sa.Column('units', sa.String)
  signal_base_amount = sa.Column('signal_base_amount', NumpyType)
  signal_base_units = sa.Column('signal_base_units', sa.String)

  def __init__(self,
      amount,
      units,
      signal_base_amount,
      signal_base_units):
    self.amount = np.array(amount)
    self.units = units
    self.signal_base_amount = np.array(signal_base_amount)
    self.signal_base_units = signal_base_units

  def getJSON(self):
    return json.dumps({
      'amount': self.start,
      'units': self.stop,
      'signal_base_amount': self.signal_base_amount,
      'signal_base_units': self.signal_base_units})

  def checksum_json(self):
    return checksum_json(self)


class DTOSpikeTimes(Base):
  __tablename__ = PREFIX + 'spike_times'
  key = sa.Column('key', sa.Integer, primary_key=True)
  uuid = sa.Column('uuid', GUID, unique=True,
      default=uuid.uuid4)
  amount = sa.Column('amount', NumpyType)
  units = sa.Column('units', sa.String)

  def __init__(self,
      amount,
      units):
    self.amount = np.array(amount)
    self.units = units

  def checksum_json(self):
    return checksum_json(self)


class DTORegularlySampledTimeSeries(Base):
  __tablename__ = PREFIX + 'regularly_sampled_time_series'

  key = sa.Column(
      'key',
      sa.Integer,
      primary_key=True)
  uuid = sa.Column('uuid', GUID, unique=True,
      default=uuid.uuid4)
  amount = sa.Column('amount', NumpyType)
  units = sa.Column('units', sa.String)
  start = sa.Column('start', sa.Float)
  stop = sa.Column('stop', sa.Float)
  time_units = sa.Column('time_units', sa.String)

  def __init__(self, amount, units, start, stop, time_units):
    self.amount = np.array(amount)
    self.units = units
    self.start = start
    self.stop = stop
    self.time_units = time_units

  def checksum_json(self):
    return checksum_json(self)


class DTOBinnedSpikes(Base):
  """
  ``BinnedSpikes`` are a special case of ``RegularlySamgledSignal`` with
  integer values for ``signals`` and bin-times as ``signal_base``.
  """
  __tablename__ = PREFIX + 'binned_spikes'
  key = sa.Column(
      'key',
      sa.Integer,
      primary_key=True)
  uuid = sa.Column('uuid', GUID, unique=True,
      default=uuid.uuid4)
  amount = sa.Column('amount', NumpyType)
  start = sa.Column('start', sa.Float)
  stop = sa.Column('stop', sa.Float)
  time_units = sa.Column('time_units', sa.String)

  def __init__(self, amount, start, stop, time_units):
    self.amount = np.array(amount, 'int')
    self.start = start
    self.stop = stop
    self.time_units = time_units

  def checksum_json(self):
    return checksum_json(self)

def initialize_sql(engine):
  DBSession.configure(bind=engine)
  Base.metadata.bind = engine
  Base.metadata.create_all(engine)

if __name__ == "__main__":
  from datajongleur.utils.sa import get_test_session
  session = get_test_session(Base)
