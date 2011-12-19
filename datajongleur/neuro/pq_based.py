from sqlalchemy.orm import object_session
import numpy as np
import json
import pdb

import datajongleur.beanbags.interfaces as i
from datajongleur.beanbags.quantity import Quantity 
from datajongleur.beanbags.quantity import InfoQuantity
from datajongleur.neuro.models import *
#from datajongleur import DBSession


@addDBAccess(DTOTimePoint, 'time_point_key')
@passLKeyDTO
class TimePoint(InfoQuantity):
  _DTO = DTOTimePoint

  def getTime(self):
    return self 

  def __repr__(self):
    return "%s(%s, %r)" %(
        self.__class__.__name__,
        self.getAmount(),
        self.getUnits())

  def __hash__(self):
    # different from `getHashValue` as python-hashs should be integer for usage
    # for collections
    return hash(self.__repr__())

  def getHashValue(self):
    return sha1(self.__repr__()).hexdigest()

  # ------- Mapping Properties -----------
  time = property(
      getTime,
      i.Value.throwSetImmutableAttributeError)


@addDBAccess(DTOPeriod, 'period_key')
@passLKeyDTO
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

  def getDTO(self):
    return self._dto

  def getStart(self):
    return self[0]

  def getStop(self):
    return self[1]

  def getLength(self):
    return np.diff(self)[0]

  def __hash__(self):
    # different from `getHashValue` as python-hashs should be integer for usage
    return hash(self.__repr__())
  
  def getHashValue(self):
    return sha1(self.__repr__()).hexdigest()
  
  def __str__(self):
    return """\
  start:  %s
  stop:   %s
  length: %s    
  """ %(self.start, self.stop, self.length)
  
  def __repr__(self):
    return '%s([%s, %s], %r)' %(
        self.__class__.__name__,
        self.amount[0],
        self.amount[1],
        self.units)

  # ------- Mapping Properties -----------
  start = property(getStart)
  stop = property(getStop)
  length = property(getLength)


@addDBAccess(DTOSampledTimeSeries, 'sampled_time_series_key')
@passLKeyDTO
class SampledTimeSeries(Quantity, i.SampledSignal, i.Interval):
  def __new__(cls,
      signal,
      signal_units,
      signal_base,
      signal_base_units,
      **kwargs # to catch e.g. ``dtype``, ``copy`` attributes
      ):
    #: Call the parent class constructor
    assert len(signal) == len(signal_base),\
        "len(signal) != len(signal_base)."
    dto = DTOSampledTimeSeries(
        signal,
        signal_units,
        signal_base,
        signal_base_units)
    obj = cls.newByDTO(dto)
    return obj

  @classmethod
  def newByDTO(cls, dto):
    obj = Quantity(
        dto.signal,
        dto.signal_units).view(cls)
    obj._signal = obj.view(Quantity)
    obj._signal_base = Quantity(
        dto.signal_base,
        dto.signal_base_units)
    obj._dto_sampled_time_series = dto
    return obj

  def getDTO(self):
    return self._dto_sampled_time_series

  # ----- Implementing Interval ------
  def getStart(self):
    return self._signal_base.min()

  def getStop(self):
    return self._signal_base.max()

  def getLength(self):
    return self.stop - self.start

  # ----- Implementing SampledSignal  ------
  def getSignal(self):
    return self._signal

  def getSignalBase(self):
    return self._signal_base

  def getNSamplingPoints(self):
    return Quantity(len(self.signal))

  # ----- Implementing Value  ------
  def __str__(self):
    return """
  signal:          %s,
  signalbase:      %s,
  start:           %s,
  stop:            %s,
  length:          %s,
  n sample points: %s""" %(
   self.signal,
   self.signal_base,
   self.start,
   self.stop,
   self.length,
   self.n_sampling_points,
   )

  def __repr__(self):
    return '%s(%r, %r)' %(
        self.__class__.__name__,
        self.amount,
        self.units,
        )

  def getHashValue(self):
    return sha1(self.__repr__()).hexdigest()

  def __hash__(self):
    return hash(self.__repr__())

  # ------- Mapping Properties ----------
  signal = property(
      getSignal,
      i.Value.throwSetImmutableAttributeError)
  signal_base = property(
      getSignalBase,
      i.Value.throwSetImmutableAttributeError)
  n_sampling_points = property(
      getNSamplingPoints,
      i.Value.throwSetImmutableAttributeError)
  start = property(
      getStart,
      i.Value.throwSetImmutableAttributeError)
  stop = property(
      getStop,
      i.Value.throwSetImmutableAttributeError)
  length = property(
      getLength,
      i.Value.throwSetImmutableAttributeError)

  
@addDBAccess(DTOSpikeTimes, 'spike_times_key')
@passLKeyDTO
class SpikeTimes(SampledTimeSeries):
  """
  ``SpikeTimes`` are a special case of ``SampledSignal`` with value 1 for
  ``signals`` and spike times as ``signal_base``, respectively.
  """
  def __new__(cls,
      spike_times,
      spike_times_units,
      **kwargs # to catch e.g. ``dtype``, ``copy`` attributes
      ):
    #: Call the parent class constructor
    dto = DTOSpikeTimes(
        spike_times,
        spike_times_units)
    obj = cls.newByDTO(dto)
    obj._dto_spike_times = dto
    return obj

  @classmethod
  def newByDTO(cls, dto):
    obj = Quantity(
        dto.spike_times,
        dto.spike_times_units).view(cls)
    obj._signal = Quantity(np.ones(len(
      dto.spike_times)), dtype=bool)
    obj._signal_base = Quantity(
        dto.spike_times, 
        dto.spike_times_units)
    obj._dto_sampled_time_series = dto
    return obj

  def getDTO(self):
    return self._dto_sampled_time_series

  
@addDBAccess(DTORegularlySampledTimeSeries,
    'regularly_sampled_time_series_key')
@passLKeyDTO
class RegularlySampledTimeSeries(SampledTimeSeries, i.RegularlySampledSignal):
  def __new__(cls,
      sampled_signal,
      sampled_signal_units,
      start,
      stop,
      time_units,
      **kwargs # to catch e.g. ``dtype``, ``copy`` attributes
      ):
    #: Call the parent class constructor
    dto = DTORegularlySampledTimeSeries(
        sampled_signal,
        sampled_signal_units,
        start,
        stop,
        time_units)
    obj = cls.newByDTO(dto)
    obj._dto_regularly_sampled_time_series = dto
    return obj

  @classmethod
  def newByDTO(cls, dto):
    obj = Quantity(
        dto.sampled_signal,
        dto.sampled_signal_units).view(cls)
    obj._signal = obj.view(Quantity)
    obj._start = Quantity(
        dto.start,
        dto.time_units)
    obj._stop = Quantity(
        dto.stop,
        dto.time_units)
    obj._dto_regularly_sampled_time_series = dto
    return obj

  def getDTO(self):
    return self._dto_regularly_sampled_time_series

  def getSelf(self):
    return self

  # ----- Implementation Period (diff. SampledTimeSeries)------
  def getStart(self):
    return self._start

  def getStop(self):
    return self._stop

  def getSignalBase(self):
    return np.linspace(self.start, self.stop, self.n_sample_points)
  
  # ----- Implementing RegularlySampledSignal (diff. SampledTimeSeries) ----
  def getSamplingRate(self):
    return (self.n_sample_points - 1.0) / self.length
  
  def getStepSize(self):
    return 1 / self.sampling_rate

  def getNSamplePoints(self):
    return Quantity(len(self.signal))

  # ----- Implementing Value  ------
  def __str__(self):
    return str(self.__dict__)
    return """
        signal:          %s,
        signalbase:      %s,
        start:           %s,
        stop:            %s,
        length:          %s,
        sampling rate:   %s,
        step size:       %s,
        n sample points: %s""" %(
           self.signal,
           self.signal_base,
           self.start,
           self.stop,
           self.length,
           self.sampling_rate,
           self.step_size,
           self.n_sample_points,
           )

  def __repr__(self):
    return '%r(%s, %r, %s, %s, %r)' %(
        self.__class__.__name__,
        self.signal.amount,
        self.signal.units,
        self.start.amount,
        self.stop.amount,
        self.stop.units)

  def getHashValue(self):
    return sha1(self.__repr__()).hexdigest()

  def __hash__(self):
    return hash(self.__repr__())

  # ------- Mapping Properties ----------
  stop = property(
      getStop,
      i.Value.throwSetImmutableAttributeError)
  start = property(
      getStart,
      i.Value.throwSetImmutableAttributeError)
  n_sample_points = property(
      getNSamplePoints,
      i.Value.throwSetImmutableAttributeError)
  signal_base = property(
      getSignalBase,
      i.Value.throwSetImmutableAttributeError)
  sampling_rate = property(
      getSamplingRate,
      i.Value.throwSetImmutableAttributeError)
  step_size = property(
      getStepSize,
      i.Value.throwSetImmutableAttributeError)


@addDBAccess(DTOBinnedSpikes, 'binned_spikes_key')
@passLKeyDTO
class BinnedSpikes(RegularlySampledTimeSeries):
  """
  ``BinnedSpikes`` are a special case of ``RegularlySamgledSignal`` with
  integer values for ``signals`` and bin-times as ``signal_base``.
  """
  def __new__(
      cls,
      sampled_signal,
      start,
      stop,
      time_units,
      **kwargs # to catch e.g. ``dtype``, ``copy`` attributes
      ):
    #: Call the parent class constructor
    assert np.array(sampled_signal).dtype == 'int',\
        "sample signal has to be of type 'int'"
    dto = DTOBinnedSpikes(
        sampled_signal,
        start,
        stop,
        time_units)
    obj = cls.newByDTO(dto)
    obj._dto_binned_spikes = dto    
    return obj
  
  @classmethod
  def newByDTO(cls, dto):
    obj = Quantity(
        dto.sampled_signal).view(cls)
    obj._signal = obj.view(Quantity)
    obj._start = Quantity(
        dto.start,
        dto.time_units)
    obj._stop = Quantity(
        dto.stop,
        dto.time_units)
    obj._dto_binned_spikes = dto
    return obj

  def getDTO(self):
    return self._dto_binned_spikes

  def __repr__(self):
    return '%s(%r, %r, %r, %r)' %(
        self.__class__.__name__,
        self.signal.amount,
        self.start.amount,
        self.stop.amount,
        self.stop.units)

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
