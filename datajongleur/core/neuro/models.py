import sqlalchemy as sa
import sqlalchemy.orm as orm
import numpy as np
import uuid
from datajongleur import Base
from datajongleur.utils.sa import NumpyType, UUID
from datajongleur.core.models import Identity
from datajongleur.core.models import PREFIX as BB_PREFIX
import datajongleur.core.models as core_m
import datajongleur.core.neuro.beanbags as neuro_bb
import datajongleur.core.neuro.beanbags as core_bb
from datajongleur.utils.sa import addInfoQuantityDBAccess, dtoAttrs2Info

PREFIX = 'dj_neuro_'

@addInfoQuantityDBAccess
class TimePoint(neuro_bb.TimePoint, core_m.Identity):
  __tablename__ =  PREFIX + 'time_points'
  __mapper_args__ = {'polymorphic_identity': 'TimePoint'}
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  _amount = sa.Column('amount', sa.Float)
  _units = sa.Column('units', sa.String)


@addInfoQuantityDBAccess
class Interval(neuro_bb.Interval, core_m.Identity):
  __tablename__ = PREFIX + 'periods'
  __mapper_args__ = {'polymorphic_identity': 'Period'}
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  _start = sa.Column('start', sa.Float)
  _stop = sa.Column('stop', sa.Float)
  _units = sa.Column('units', sa.String)


@addInfoQuantityDBAccess
class SampledTimeSeries(neuro_bb.SampledTimeSeries, core_m.Identity):
  __tablename__ = PREFIX + 'sampled_time_series'
  __mapper_args__ = {'polymorphic_identity': 'SampledTimeSeries'}
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  _amount = sa.Column('amount', NumpyType)
  _units = sa.Column('units', sa.String)
  _signal_base_amount = sa.Column('signal_base_amount', NumpyType)
  _signal_base_units = sa.Column('signal_base_units', sa.String)


@addInfoQuantityDBAccess
class SpikeTimes(neuro_bb.SpikeTimes, core_m.Identity):
  __tablename__ = PREFIX + 'spike_times'
  __mapper_args__ = {'polymorphic_identity': 'SpikeTimes'}
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  _amount = sa.Column('amount', NumpyType)
  _units = sa.Column('units', sa.String)

  def checksum_json(self):
    return checksum_json(self)


class DTORegularlySampledTimeSeries(Identity):
  __tablename__ = PREFIX + 'regularly_sampled_time_series'
  __mapper_args__ = {'polymorphic_identity': 'RegularlySampledTimeSeries'}
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
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


class DTOBinnedSpikes(Identity):
  """
  ``BinnedSpikes`` are a special case of ``RegularlySamgledSignal`` with
  integer values for ``signals`` and bin-times as ``signal_base``.
  """
  __tablename__ = PREFIX + 'binned_spikes'
  __mapper_args__ = {'polymorphic_identity': 'BinnedSpikes'}
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  amount = sa.Column('amount', NumpyType)
  start = sa.Column('start', sa.Float)
  stop = sa.Column('stop', sa.Float)
  time_units = sa.Column('time_units', sa.String)

  def __init__(self, amount, units, start, stop, time_units):
    self.amount = np.array(amount, 'int')
    self.start = start
    self.stop = stop
    self.units = ''
    self.time_units = time_units

  def checksum_json(self):
    return checksum_json(self)

if __name__ == "__main__":
  from datajongleur.utils.sa import get_test_session
  session = get_test_session(Base)
