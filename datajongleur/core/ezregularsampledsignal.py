class EZRegularlySampledTimeSeries():
  def __init__(self, signal, t_start, t_stop):
    if t_start.units != t_stop.units:
      raise AttributeError("t_start.units != t_stop.units")
    self._signal = signal
    self._t_start = t_start
    self._t_stop = t_stop
    self._quantity_class = signal.__class__
    self._one = self._quantity_class(1, "1")

  # -------------------------
  # define properties -------
  # -------------------------
  def getSignal(self):
    return self._signal
  signal = property(fget=getSignal)

  def getSamplingBase(self):
    amount = np.linspace(
        self.t_start.amount, self.t_stop.amount, self.n_sampling_points.amount)
    units = self.t_start.units
    return self.t_start.__class__(amount, units)
  sampling_base = property(
      fget=getSamplingBase,
      doc='sampling basis')

  def getDuration(self):
    return self._t_stop - self._t_start
  duration = property(fget=getDuration, doc='duration := t_stop - t_start')

  def getTStart(self):
    return self._t_start
  t_start = property(fget=getTStart, doc='t_start')

  def getTStop(self):
    return self._t_stop
  t_stop = property(fget=getTStop, doc='t_stop')

  def getNSamplingPoints(self):
    return self._quantity_class(len(self._signal.amount), "1")
  n_sampling_points = property(fget=getNSamplingPoints,
      doc='number of samples')
  
  def getSamplingRate(self):
    return (self.n_sampling_points - self._one) / (self.t_stop - self.t_start) 
  sampling_rate = property(fget=getSamplingRate,
      doc='sampling_rate := 1 / step')

  def getStep(self):
    return (self.duration) / (self.n_sampling_points - self._one)
  step = property(fget=getStep, doc='difference of two adjacend samples')

  # ----------------------
  # setting aliases-------
  # ----------------------
  sb = sampling_base
  sr = sampling_rate
  sample_rate = sampling_rate
  times = sampling_base


if __name__ == "__main__":
  import numpy as np
  from quantity import EZQuantity as Quantity
  signal = Quantity(np.array([1,2,3,4,5,6.8]), "mV")
  #signal = Quantity([1,2,3,4,5,6.8], "mV")
  t_start = Quantity(5, "ms")
  t_stop = Quantity(12, "ms")
  RSTS = EZRegularlySampledTimeSeries(signal, t_start, t_stop)
