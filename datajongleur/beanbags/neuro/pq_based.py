from sqlalchemy.orm import object_session
from quantities import Quantity
import numpy as np
import json
import pdb

import datajongleur.beanbags.interfaces as i
from datajongleur.beanbags.pq_based import InfoQuantity
from .models import *
from datajongleur import bbc
from datajongleur.utils.miscellaneous import *
from datajongleur.utils.sa import addInfoQuantityDBAccess, dtoAttrs2Info


@addInfoQuantityDBAccess
@addAttributesProxy(['uuid'], '_dto')
class TimePoint(InfoQuantity):
  _DTO = DTOTimePoint

  @property
  def signal(self):
    return self.view(Quantity) 

  @property
  def info(self):
    return {'signal': self.signal}

@addInfoQuantityDBAccess
@addAttributesProxy(['uuid'], '_dto')
class Period(InfoQuantity, i.Interval):
  _DTO = DTOPeriod

  @classmethod
  def newByDTO(cls, dto):
    obj = Quantity(
        [dto.start, dto.stop],
        dto.units,
        ).view(cls)
    obj._dto = dto
    return obj

  def __getitem__(self, key):
    return Quantity.__getitem__(self.view(Quantity), key)
  
  @property
  def start(self):
    return self[0]

  @property
  def stop(self):
    return self[1]

  @property
  def length(self):
    return np.diff(self)[0]

  @property
  def signal(self):
    return self.view(Quantity) 

  @property
  def info(self):
    return {'signal': self.signal}


@addInfoQuantityDBAccess
@addAttributesProxy(['uuid'], '_dto')
class SampledTimeSeries(InfoQuantity, i.SampledSignal, i.Interval):
  _DTO = DTOSampledTimeSeries

  # ----- Implementing Interval ------
  @property
  def start(self):
    return self.info['signal_base'].min()

  @property
  def stop(self):
    return self.info['signal_base'].max()

  @property
  def length(self):
    return self.stop - self.start

  # ----- Implementing SampledSignal  ------
  @property
  def signal(self):
    return self.info['signal']

  @property
  def signal_base(self):
    return self.info['signal_base']

  @property
  def n_sampling_points(self):
    return Quantity(len(self), '')

  @property
  def info(self):
    signal = self.view(Quantity)
    signal_base = Quantity(
      self._dto.signal_base_amount,
      self._dto.signal_base_units)
    signal_base.setflags(write=False)
    return {
        'signal': signal,
        'signal_base': signal_base}


@addInfoQuantityDBAccess
@addAttributesProxy(['uuid'], '_dto')
class SpikeTimes(SampledTimeSeries):
  """
  ``SpikeTimes`` are a special case of ``SampledSignal`` with value 1 for
  ``signals`` and spike times as ``signal_base``, respectively.
  """
  _DTO = DTOSpikeTimes

  @property
  def info(self):
    signal = Quantity(np.ones(len(self), dtype=bool))
    signal_base = self.view(Quantity)
    return {
        'signal': signal,
        'signal_base': signal_base}
 

@addInfoQuantityDBAccess
@addAttributesProxy(['uuid'], '_dto')
class RegularlySampledTimeSeries(SampledTimeSeries, i.RegularlySampledSignal):
  _DTO = DTORegularlySampledTimeSeries

  # ----- Implementation Period (diff. SampledTimeSeries)------
  @property
  def start(self):
    return self.info['start']

  @property
  def stop(self):
    return self.info['stop']

  # ----- Implementing RegularlySampledSignal (diff. SampledTimeSeries) ----
  @property
  def sampling_rate(self):
    return (self.n_sample_points - 1.0) / self.length
  
  @property
  def step_size(self):
    return 1 / self.sampling_rate

  @property
  def n_sample_points(self):
    return Quantity(len(self.amount), "")

  # ----- Implementing Value  ------
  def __str__(self):
    return str(self.__dict__)

  @property
  def info(self):
    signal = self.view(Quantity)
    start = Quantity(self._dto.start, self._dto.time_units)
    stop = Quantity(self._dto.stop, self._dto.time_units)
    signal_base = Quantity(
        np.linspace(start, stop, self.n_sample_points),
        self._dto.time_units)
    return {
        'signal': signal,
        'signal_base': signal_base,
        'start': start,
        'stop': stop}
    

@addInfoQuantityDBAccess
@addAttributesProxy(['uuid'], '_dto')
class BinnedSpikes(RegularlySampledTimeSeries):
  """
  ``BinnedSpikes`` are a special case of ``RegularlySampledSignal`` with
  integer values for ``signals`` and bin-times as ``signal_base``.
  """
  _DTO = DTOBinnedSpikes

beanbags = [
    TimePoint,
    Period,
    SampledTimeSeries,
    SpikeTimes,
    RegularlySampledTimeSeries,
    BinnedSpikes]

for beanbag in beanbags:
  bbc.register_bb(beanbag)


if __name__ == '__main__':
  from datajongleur.utils.sa import get_test_session
  session = get_test_session(Base)
  # Test DTOTimePoint
  a_dto = DTOTimePoint(1, 'ms')
  # Test TimePoint
  a = TimePoint.newByDTO(a_dto)
  a.save
  spike_times = SpikeTimes([1.3, 1.9, 2.5], "ms")
  p = Period(1,2,"s")
  rsts = RegularlySampledTimeSeries([1,2,3],"mV", 1, 5, "s")
  sts = SampledTimeSeries([1,2,3], 'mV', [1,4,7], 's')
  if False:
    q = Quantity([1,2,3], 'mV')
    b = TimePoint(2, "ms")
    c = TimePoint(2, "ms")
    session.add(a)
    session.add(b)
    session.add(c)
    session.commit()
    print (a==b)
    print (b==c)
    session.add(p)
    session.add(q)
    session.add(spike_times)
    session.add(rsts)
    session.add(sts)
    session.commit ()
    print (rsts * 2)
