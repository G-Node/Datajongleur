from sqlalchemy.orm import object_session
import numpy as np
import json
import pdb

import datajongleur.beanbags.interfaces as i
from datajongleur.beanbags.quantity import Quantity 
from datajongleur.beanbags.quantity import InfoQuantity
from datajongleur.ext.neuro.models import *
#from datajongleur import DBSession

@addInfoQuantityDBAccess()
@passAttrDTO
class TimePoint(InfoQuantity):
  _DTO = DTOTimePoint

  def getTime(self):
    return self 

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


@addInfoQuantityDBAccess()
@passAttrDTO
class Period(InfoQuantity, i.Interval):
  _DTO = DTOPeriod

  @classmethod
  def newByDTO(cls, dto):
    obj = Quantity(
        [dto.start, dto.stop],
        dto.units,
        ).view(cls)
    obj._dto = dto
    obj._info_attributes = {}
    return obj

  def __getitem__(self, key):
    return Quantity.__getitem__(self.view(Quantity), key)

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
  """  
  def __repr_main__(self):
    return '%s\n([%s, %s], %r)' %(
        self.__class__.__name__,
        self.amount[0],
        self.amount[1],
        self.units)
  """
  # ------- Mapping Properties -----------
  start = property(getStart)
  stop = property(getStop)
  length = property(getLength)


@addInfoQuantityDBAccess()
@passAttrDTO
class SampledTimeSeries(InfoQuantity, i.SampledSignal, i.Interval):
  _DTO = DTOSampledTimeSeries
  def __new__(cls,
      amount,
      units,
      signal_base_amount=None,
      signal_base_units=None,
      **kwargs # to catch e.g. ``dtype``, ``copy`` attributes
      ):
    if not (signal_base_amount and signal_base_units):
      return Quantity(amount, units)
    #: Call the parent class constructor
    assert len(amount) == len(signal_base_amount),\
        "len(signal) != len(signal_base_amount)."
    dto = cls._DTO(
        amount,
        units,
        signal_base_amount,
        signal_base_units)
    obj = cls.newByDTO(dto)
    return obj

  @classmethod
  def newByDTO(cls, dto):
    obj = Quantity(
        dto.amount,
        dto.units).view(cls)
    obj._info_attributes = {}
    obj._info_attributes['signal_base'] = Quantity(
        dto.signal_base_amount,
        dto.signal_base_units)
    obj._dto = dto
    return obj

  # ----- Implementing Interval ------
  def getStart(self):
    return self._info_attributes['signal_base'].min()

  def getStop(self):
    return self._info_attributes['signal_base'].max()

  def getLength(self):
    return self.stop - self.start

  # ----- Implementing SampledSignal  ------
  def getSignalBase(self):
    return self._info_attributes['signal_base']

  def getNSamplingPoints(self):
    return Quantity(len(self), '')

  # ----- Implementing Value  ------
  def __str__(self):
    return """
  amount:          %s,
  units:           %s,
  signalbase:      %s,
  start:           %s,
  stop:            %s,
  length:          %s,
  n sample points: %s""" %(
   self.amount,
   self.units,
   self.signal_base,
   self.start,
   self.stop,
   self.length,
   self.n_sampling_points,
   )

  def getHashValue(self):
    return sha1(self.__repr__()).hexdigest()

  def __hash__(self):
    return hash(self.__repr__())

  # ------- Mapping Properties ----------
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

  
@addInfoQuantityDBAccess()
@passAttrDTO
class SpikeTimes(SampledTimeSeries):
  """
  ``SpikeTimes`` are a special case of ``SampledSignal`` with value 1 for
  ``signals`` and spike times as ``signal_base``, respectively.
  """
  _DTO = DTOSpikeTimes
  def __new__(cls,
      amount,
      units,
      **kwargs # to catch e.g. ``dtype``, ``copy`` attributes
      ):
    #: Call the parent class constructor
    dto = cls._DTO(
        amount,
        units)
    obj = cls.newByDTO(dto)
    return obj

  @classmethod
  def newByDTO(cls, dto):
    obj = Quantity(
        dto.amount,
        dto.units).view(cls)
    obj._info_attributes = {}
    obj._info_attributes['signal'] = Quantity(np.ones(len(
      dto.amount), dtype=bool), '')#, dtype=bool)
    obj._info_attributes['signal_base'] = Quantity(
        dto.amount, 
        dto.units)
    obj._dto = dto
    return obj

  def getSignal(self):
    return self._info_attributes['signal']
  signal = property(
      getSignal,
      i.Value.throwSetImmutableAttributeError)
  
@addInfoQuantityDBAccess()
@passAttrDTO
class RegularlySampledTimeSeries(SampledTimeSeries, i.RegularlySampledSignal):
  _DTO = DTORegularlySampledTimeSeries
  def __new__(cls,
      amount,
      units,
      start,
      stop,
      time_units,
      **kwargs # to catch e.g. ``dtype``, ``copy`` attributes
      ):
    #: Call the parent class constructor
    dto = DTORegularlySampledTimeSeries(
        amount,
        units,
        start,
        stop,
        time_units)
    obj = cls.newByDTO(dto)
    return obj

  @classmethod
  def newByDTO(cls, dto):
    obj = Quantity(
        dto.amount,
        dto.units).view(cls)
    obj._info_attributes = {}
    obj._info_attributes['start'] = Quantity(
        dto.start,
        dto.time_units)
    obj._info_attributes['stop'] = Quantity(
        dto.stop,
        dto.time_units)
    obj._dto = dto
    return obj

  def getSelf(self):
    return self

  # ----- Implementation Period (diff. SampledTimeSeries)------
  def getStart(self):
    return self._info_attributes['start']

  def getStop(self):
    return self._info_attributes['stop']

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

  """
  def __repr__(self):
    return '%r(%s, %r, %s, %s, %r)' %(
        self.__class__.__name__,
        self.signal.amount,
        self.signal.units,
        self.start.amount,
        self.stop.amount,
        self.stop.units)
  """

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


@addInfoQuantityDBAccess()
@passAttrDTO
class BinnedSpikes(RegularlySampledTimeSeries):
  """
  ``BinnedSpikes`` are a special case of ``RegularlySampledSignal`` with
  integer values for ``signals`` and bin-times as ``signal_base``.
  """
  _DTO = DTOBinnedSpikes
  def __new__(
      cls,
      amount,
      start,
      stop,
      time_units,
      **kwargs # to catch e.g. ``dtype``, ``copy`` attributes
      ):
    if not (start and stop and time_units):
      return Quantity(amount, '')
    #: Call the parent class constructor
    assert np.array(amount).dtype == 'int',\
        "sample signal has to be of type 'int'"
    dto = DTOBinnedSpikes(
        amount,
        start,
        stop,
        time_units)
    obj = cls.newByDTO(dto)
    return obj
  
  @classmethod
  def newByDTO(cls, dto):
    obj = Quantity(
        dto.amount, '').view(cls)
    obj._info_attributes = {}
    obj._info_attributes['start'] = Quantity(
        dto.start,
        dto.time_units)
    obj._info_attributes['stop'] = Quantity(
        dto.stop,
        dto.time_units)
    obj._dto = dto
    return obj
  """
  def __repr__(self):
    return '%s(%r, %r, %r, %r)' %(
        self.__class__.__name__,
        self.signal.amount,
        self.start.amount,
        self.stop.amount,
        self.stop.units)
  """

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
