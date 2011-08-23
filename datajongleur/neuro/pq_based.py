from datajongleur.core.quantity import QuantitiesAdapter as Quantity
import numpy as np
import datajongleur.core.interfaces as i

class Moment(Quantity):
  def __new__(cls, time, units):
    obj = Quantity(time, units).view(Moment)
    return obj

  def getTime(self):
    return self 

  def __repr__(self):
    return "Moment(%s, %r)" %(self.getAmount(), self.getUnits())

  # ------- Mapping Properties -----------
  time = property(
      getTime,
      i.Value.throwSetImmutableAttributeError)


class Period(i.Interval):
  def __init__(self, start, stop, units):
    self._start_stop = Quantity([start, stop], units)

  def getStart(self):
    return self._start_stop[0]

  def getStop(self):
    return self._start_stop[1]

  def getLength(self):
    return np.diff(self._start_stop)[0]

  def __hash__(self):
    return hash(self.__repr__())

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


class SampledTimeSeries(Quantity, i.SampledSignal, i.Interval):
  def __new__(cls,
      signal,
      signal_units,
      signal_base,
      signal_base_units):
    #: Call the parent class constructor
    assert len(signal) == len(signal_base),\
        "len(signal) != len(signal_base)."
    obj = Quantity(signal, signal_units).view(SampledTimeSeries)
    obj._signal = obj.view(Quantity)
    obj._signal_base = Quantity(signal_base, signal_base_units)
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

  
class SpikeTimes(SampledTimeSeries):
  """
  ``SpikeTimes`` are a special case of ``SampledSignal`` with value 1 for
  ``signals`` and spike times as ``signal_base``, respectively.
  """
  def __new__(cls,
      spiketimes,
      spiketimes_units):
    #: Call the parent class constructor
    obj = Quantity(spiketimes, spiketimes_units).view(SpikeTimes)
    obj._signal = Quantity(np.ones(len(spiketimes)), dtype=bool)
    obj._signal_base = Quantity(spiketimes, spiketimes_units)
    return obj

  
class RegularlySampledTimeSeries(SampledTimeSeries, i.RegularlySampledSignal):
  def __new__(cls, sample_signal, sample_units, start, stop, time_units):
    #: Call the parent class constructor
    obj = Quantity(sample_signal, sample_units).view(cls)
    obj._signal = obj.view(Quantity)
    obj._start = Quantity(start, time_units)
    obj._stop = Quantity(stop, time_units)
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


class BinnedSpikes(RegularlySampledTimeSeries):
  """
  ``BinnedSpikes`` are a special case of ``RegularlySamgledSignal`` with
  integer values for ``signals`` and bin-times as ``signal_base``.
  """
  def __new__(cls, sample_signal, start, stop, time_units):
    #: Call the parent class constructor
    assert np.array(sample_signal).dtype == 'int',\
        "sample signal has to be of type 'int'"
    obj = Quantity(sample_signal).view(cls)
    obj._signal = obj.view(Quantity)
    obj._start = Quantity(start, time_units)
    obj._stop = Quantity(stop, time_units)
    return obj

  def __repr__(self):
    return '%s(%r, %r, %r, %r, %r)' %(
        self.__class__.__name__,
        self.signal.amount,
        self.start.amount,
        self.stop.amount,
        self.stop.units)

if __name__ == '__main__':
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
