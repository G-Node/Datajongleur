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

@addInfoQuantityDBAccess
@addAttributesProxy(['uuid'], '_dto')


@addInfoQuantityDBAccess
@addAttributesProxy(['uuid'], '_dto')
class SpikeTimes(SampledTimeSeries):
  """
  ``SpikeTimes`` are a special case of ``SampledSignal`` with value 1 for
  ``signals`` and spike times as ``signal_base``, respectively.
  """
  _DTO = DTOSpikeTimes


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
