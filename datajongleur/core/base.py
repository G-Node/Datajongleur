import interfaces as i

class Interval(i.Interval):
  def getStart(self):
    return self._start
  start = property(getStart)

  def getStop(self):
    return self._stop
  stop = property(getStop)

  def getLength(self):
    return self._stop - self._start
  length = property(getLength)

  def __hash__(self):
    return hash(self.__repr__())

  def __str__(self):
    return """\
start:  %s
stop:   %s
length: %s    
""" %(self.start, self.stop, self.length)

  def __repr__(self):
    return '%s(%r, %r, %r)' %(
        self.__class__.__name__,
        self.getStart().getAmount(),
        self.getStop().getAmount(),
        self.getStart().getUnits())

class SampledSignal(i.SampledSignal):
  def getSignal(self):
    return self._signal
  signal = property(
      getSignal,
      i.BaseValue.setImmutableAttribute)

  def getSignalBase(self):
    return np.linspace(self.start, self.stop, self.n_sample_points)
  signal_base = property(
      getSignalBase,
      i.BaseValue.setImmutableAttribute)

  # ----- Implementing Value-Interface  ------
  def __str__(self):
    return """
signal:          %s,
signalbase:      %s,
n sample points: %s""" %(
   self.signal,
   self.signal_base,
   self.n_sample_points,
   )

  def __repr__(self):
    return '%s(%r, %r, %r, %r)' %(
        self.__class__.__name__,
        self.signal.amount,
        self.signal.units,
        self.signal_base.amount,
        self.signal_base.units,
        )

  def __hash__(self):
    return hash(self.__repr__())


class RegularlySampledSignal(SampledSignal, i.RegularlySampledSignal):
  def getSamplingRate(self):
    return self._sampling_rate
  sampling_rate = property(
      getSamplingRate,
      i.BaseValue.setImmutableAttribute)

  def getStepSize(self):
    return 1 / self.sampling_rate
  step_size = property(
      getStepSize,
      i.BaseValue.setImmutableAttribute)

  def getNSamplePoints(self):
    return Quantity(len(self.signal))
  n_sample_points = property(
      getNSamplePoints,
      i.BaseValue.setImmutableAttribute)

  # ----- Implementing Value-Interface  ------
  def __str__(self):
    return """
signal:          %s,
signalbase:      %s,
sampling rate:   %s,
step size:       %s,
n sample points: %s""" %(
   self.signal,
   self.signal_base,
   self.sampling_rate,
   self.step_size,
   self.n_sample_points,
   )

  def __repr__(self):
    return '%s(%r, %r, %r, %r, %r)' %(
        self.__class__.__name__,
        self.signal.amount,
        self.signal.units,
        self.start.amount,
        self.stop.amount,
        self.stop.units)

  def __hash__(self):
    return hash(self.__repr__())
