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

  def getKey(self):
    try:
      return self.key
    except:
      print "No key available, yet!"

  def __repr__(self):
    return "%s(%s, %r)" %(
        self.__class__.__name__,
        self.amount,
        self.units)

class DTOPeriod(Base):
  __tablename__ = PREFIX + 'periods'
  
  period_key = sa.Column('period_key', sa.Integer, primary_key=True)
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

  def getKey(self):
    try:
      return self.period_key
    except:
      print "No key available, yet!"

  def __repr__(self):
    return "%s(start=%s, stop=%s, units=%r)" %(
        self.__class__.__name__,
        self.start,
        self.stop,
        self.units)


class DTOSampledTimeSeries(Base):
  __tablename__ = PREFIX + 'sampled_time_series'
  sampled_time_series_key = sa.Column(
      'sampled_time_series_key',
      sa.Integer,
      primary_key=True)
  signal = sa.Column('signal', NumpyType)
  signal_units = sa.Column('signal_units', sa.String)
  signal_base = sa.Column('signal_base', NumpyType)
  signal_base_units = sa.Column('signal_base_units', sa.String)

  def __init__(self,
      signal,
      signal_units,
      signal_base,
      signal_base_units):
    self.signal = np.array(signal)
    self.signal_units = signal_units
    self.signal_base = np.array(signal_base)
    self.signal_base_units = signal_base_units

  def getJSON(self):
    return json.dumps({
      'signal': self.start,
      'signal_units': self.stop,
      'signal_base': self.signal_base,
      'signal_base_units': self.signal_base_units})

  def checksum_json(self):
    return checksum_json(self)

  def getKey(self):
    try:
      return self.sampled_time_series_key
    except Exception:
      print "%s, Some error happend..." %(Exception)
      return Exception


class DTOSpikeTimes(Base):
  __tablename__ = PREFIX + 'spike_times'
  spike_times_key = sa.Column('spike_times_key', sa.Integer, primary_key=True)
  spike_times = sa.Column('spike_times', NumpyType)
  spike_times_units = sa.Column('spike_times_units', sa.String)

  def __init__(self,
      spike_times,
      spike_times_units):
    self.spike_times = np.array(spike_times)
    self.spike_times_units = spike_times_units

  def checksum_json(self):
    return checksum_json(self)

  def getKey(self):
    try:
      return self.spike_times_key
    except:
      print "No key available, yet!"


class DTORegularlySampledTimeSeries(Base):
  __tablename__ = PREFIX + 'regularly_sampled_time_series'

  regularly_sampled_time_series_key = sa.Column(
      'regularly_sampled_time_series_key',
      sa.Integer,
      primary_key=True)
  sampled_signal = sa.Column('sampled_signal', NumpyType)
  sampled_signal_units = sa.Column('sampled_signal_units', sa.String)
  start = sa.Column('start', sa.Float)
  stop = sa.Column('stop', sa.Float)
  time_units = sa.Column('time_units', sa.String)

  def __init__(self, sampled_signal, sampled_signal_units, start, stop, time_units):
    self.sampled_signal = np.array(sampled_signal)
    self.sampled_signal_units = sampled_signal_units
    self.start = start
    self.stop = stop
    self.time_units = time_units

  def checksum_json(self):
    return checksum_json(self)

  def getKey(self):
    try:
      return self.regularly_sampled_time_series_key
    except:
      print "No key available, yet!"


class DTOBinnedSpikes(Base):
  """
  ``BinnedSpikes`` are a special case of ``RegularlySamgledSignal`` with
  integer values for ``signals`` and bin-times as ``signal_base``.
  """
  __tablename__ = PREFIX + 'binned_spikes'
  binned_spikes_key = sa.Column(
      'binned_spikes_key',
      sa.Integer,
      primary_key=True)
  sampled_signal = sa.Column('sampled_signal', NumpyType)
  start = sa.Column('start', sa.Float)
  stop = sa.Column('stop', sa.Float)
  time_units = sa.Column('time_units', sa.String)

  def __init__(self, sampled_signal, start, stop, time_units):
    self.sampled_signal = np.array(sampled_signal, 'int')
    self.start = start
    self.stop = stop
    self.time_units = time_units

  def checksum_json(self):
    return checksum_json(self)

  def getKey(self):
    try:
      return self.binned_spikes_key
    except:
      print "No key available, yet!"

def initialize_sql(engine):
  DBSession.configure(bind=engine)
  Base.metadata.bind = engine
  Base.metadata.create_all(engine)

if __name__ == "__main__":
  from datajongleur.utils.sa import get_test_session
  session = get_test_session(Base)
