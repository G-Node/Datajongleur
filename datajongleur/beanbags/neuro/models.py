import sqlalchemy as sa
import sqlalchemy.orm as orm
import numpy as np
import json
import uuid
from datajongleur import Base
from datajongleur.utils.sa import NumpyType, UUID
from datajongleur.beanbags.models import DTOIdentity
from datajongleur.beanbags.models import PREFIX as BB_PREFIX
from datajongleur.utils.miscellaneous import NumericWithUnits

PREFIX = 'dj_neuro_'
from datajongleur.utils.sa import addInfoQuantityDBAccess, dtoAttrs2Info



if False:
  class DTOSpikeTimes(DTOIdentity):
    __tablename__ = PREFIX + 'spike_times'
    __mapper_args__ = {'polymorphic_identity': 'SpikeTimes'}
    uuid = sa.Column(
        sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True)
    amount = sa.Column('amount', NumpyType)
    units = sa.Column('units', sa.String)

    def __init__(self,
        amount,
        units):
      self.amount = np.array(amount)
      self.units = units

    def checksum_json(self):
      return checksum_json(self)


  class DTORegularlySampledTimeSeries(DTOIdentity):
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


  class DTOBinnedSpikes(DTOIdentity):
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
