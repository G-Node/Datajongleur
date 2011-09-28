from datajongleur.core.quantity import QuantitiesAdapter as Quantity
from hashlib import sha1
import json
import numpy as np
import datajongleur.core.interfaces as i

def checksum_json(self):
  return sha1(self.getJSON()).hexdigest()


#############
## Moment ###
#############

class MomentDTO(object):
  def __init__(self, time, units):
    self.time = time
    self.units = units

  def getJSON(self):
    return json.dumps({
      'time': self.time,
      'units': self.units})

  def checksum_json(self):
    return checksum_json(self)

  def getXML(self):
    from datajongleur.tools.xml_jongleur import dict2xml
    d = {'time': self.time, 'units': self.units}
    xml = dict2xml(d)
    xml.display()
    

class Moment(Quantity):
  def __new__(cls, time, units):
    dto = MomentDTO(time, units)
    #obj = Quantity(time, units).view(Moment)
    return cls.newByDTO(dto)
  
  @classmethod
  def newByDTO(cls, dto):
    obj = Quantity(
        dto.time,
        dto.units).view(Moment)
    obj._dto = dto
    return obj

  def getTime(self):
    return self 

  def __repr__(self):
    return "Moment(%s, %r)" %(self.getAmount(), self.getUnits())

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

############
## Period ##
############

class PeriodDTO(object):
  def __init__(self, start, stop, units):
    self.start = start
    self.stop = stop
    self.units = units

  def getJSON(self):
    return json.dumps({
      'start': self.start,
      'stop': self.stop,
      'units': self.units})

  def checksum_json(self):
    return checksum_json(self)


class Period(i.Interval):
  def __init__(self, start, stop, units):
    dto = PeriodDTO(start, stop, units)
    self.initByDTO(dto)
    

  def initByDTO(self, dto):
    self._start_stop = Quantity(
          [dto.start, dto.stop],
          dto.units)
    self._dto = dto


  def getStart(self):
    return self._start_stop[0]

  def getStop(self):
    return self._start_stop[1]

  def getLength(self):
    return np.diff(self._start_stop)[0]

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
    return '%s(%s, %s, %r)' %(
        self.__class__.__name__,
        self.getStart().getAmount(),
        self.getStop().getAmount(),
        self.getStart().getUnits())

  # ------- Mapping Properties -----------
  start = property(getStart)
  stop = property(getStop)
  length = property(getLength)


#######################
## SampledTimeSeries ##
#######################

class SampledTimeSeriesDTO(object):
  def __init__(self,
      signal,
      signal_units,
      signal_base,
      signal_base_units):
    self.signal = signal
    self.signal_units = signal_units
    self.signal_base = signal_base
    self.signal_base_units = signal_base_units

  def getJSON(self):
    return json.dumps({
      'signal': self.start,
      'signal_units': self.stop,
      'signal_base': self.signal_base,
      'signal_base_units': self.signal_base_units})

  def checksum_json(self):
    return checksum_json(self)


class SampledTimeSeries(Quantity, i.SampledSignal, i.Interval):
  def __new__(cls,
      signal,
      signal_units,
      signal_base,
      signal_base_units):
    #: Call the parent class constructor
    assert len(signal) == len(signal_base),\
        "len(signal) != len(signal_base)."
    dto = SampledTimeSeriesDTO(
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
        dto.signal_units).view(SampledTimeSeries)
    obj._signal = obj.view(Quantity)
    obj._signal_base = Quantity(
        dto.signal_base,
        dto.signal_base_units)
    return obj

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


################
## SpikeTimes ##
################
  
class SpikeTimesDTO(object):
  def __init__(self,
      spiketimes,
      spiketimes_units):
    self.spiketimes = spiketimes
    self.spiketimes_units = spiketimes_units

  def checksum_json(self):
    return checksum_json(self)

  
class SpikeTimes(SampledTimeSeries):
  """
  ``SpikeTimes`` are a special case of ``SampledSignal`` with value 1 for
  ``signals`` and spike times as ``signal_base``, respectively.
  """
  def __new__(cls,
      spiketimes,
      spiketimes_units):
    #: Call the parent class constructor
    dto = SpikeTimesDTO(
        spiketimes,
        spiketimes_units)
    obj = cls.newByDTO(dto)
    obj._dto = dto
    return obj

  @classmethod
  def newByDTO(cls, dto):
    obj = Quantity(
        dto.spiketimes,
        dto.spiketimes_units).view(cls)
    obj._signal = Quantity(np.ones(len(
      dto.spiketimes)), dtype=bool)
    obj._signal_base = Quantity(
        dto.spiketimes, 
        dto.spiketimes_units)
    return obj


#################################
## RegularlySampledTimesSeries ##
#################################
  
class RegularlySampledTimeSeriesDTO(object):
  def __init__(self, sampled_signal, sampled_signal_units, start, stop, time_units):
    self.sampled_signal = sampled_signal
    self.sampled_signal_units = sampled_signal_units
    self.start = start
    self.stop = stop
    self.time_units = time_units

  def checksum_json(self):
    return checksum_json(self)

  
class RegularlySampledTimeSeries(SampledTimeSeries, i.RegularlySampledSignal):
  def __new__(cls, sampled_signal, sampled_signal_units, start, stop, time_units):
    #: Call the parent class constructor
    dto = RegularlySampledTimeSeriesDTO(
        sampled_signal,
        sampled_signal_units,
        start,
        stop,
        time_units)
    obj = cls.newByDTO(dto)
    obj._dto = dto
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
    return obj


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
    return '%s(%s, %r, %s, %s, %r)' %(
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


##################
## BinnedSpikes ##
##################

class BinnedSpikesDTO(object):
  """
  ``BinnedSpikes`` are a special case of ``RegularlySamgledSignal`` with
  integer values for ``signals`` and bin-times as ``signal_base``.
  """
  def __init__(self, sampled_signal, start, stop, time_units):
    self.sampled_signal = sampled_signal
    self.start = start
    self.stop = stop
    self.time_units = time_units

  def checksum_json(self):
    return checksum_json(self)


class BinnedSpikes(RegularlySampledTimeSeries):
  """
  ``BinnedSpikes`` are a special case of ``RegularlySamgledSignal`` with
  integer values for ``signals`` and bin-times as ``signal_base``.
  """
  def __new__(cls, sampled_signal, start, stop, time_units):
    #: Call the parent class constructor
    assert np.array(sampled_signal).dtype == 'int',\
        "sample signal has to be of type 'int'"
    dto = BinnedSpikesDTO(
        sampled_signal,
        start,
        stop,
        time_units)
    obj = cls.newByDTO(dto)
    obj._dto = dto    
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
    return obj

  def __repr__(self):
    return '%s(%r, %r, %r, %r)' %(
        self.__class__.__name__,
        self.signal.amount,
        self.start.amount,
        self.stop.amount,
        self.stop.units)

if __name__ == '__main__':
  # Test MomentDTO
  a_dto = MomentDTO(1, 'ms')
  # Test Moment
  a = Moment(1, "ms")
  b = Moment(2, "ms")
  c = Moment(2, "ms")
  print (a==b)
  print (b==c)
  p = Period(1,2,"s")
  q = Quantity([1,2,3], 'mV')
  spiketimes = SpikeTimes([1.3, 1.9, 2.5], "ms")
  rsts = RegularlySampledTimeSeries([1,2,3],"mV", 1, 5, "s")
  sts = SampledTimeSeries([1,2,3], 'mV', [1,4,7], 's')
