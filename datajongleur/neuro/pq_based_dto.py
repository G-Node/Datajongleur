class DTO_Moment(object):
  def __init__(self, time, units, hash_value):
    self.time = time
    self.units = units
    self.hash_value = hash_value


class DTO_Period(object):
  def __init__(self, start, stop, units, hash_value):
    self.start = start
    self.stop = stop
    self.units = units
    self.hash_value = hash_value


class DTO_SampledTimeSeries(object):
  def __init__(self,
      signal,
      signal_units,
      signal_base,
      signal_base_units,
      hash_value):
    self.signal = signal
    self.signal_units = signal_units
    self.signal_base = signal_base
    self.signal_base_units = signal_base_units
    self.hash_value = hash_value

  
class DTO_SpikeTimes(object):
  def __init__(self,
      spiketimes,
      spiketimes_units):
    self.spiketimes = spiketimes
    self.spiketimes_units = spiketimes_units
    self.hash_value = hash_value

  
class DTO_RegularlySampledTimeSeries(object):
  def __init__(self, sample_signal, sample_units, start, stop, time_units):
    self.sample_signal = sample_signal
    self.sample_units = sample_units
    self.start = start
    self.stop = stop
    self.time_units = time_units


class DTO_BinnedSpikes(Object):
  """
  ``BinnedSpikes`` are a special case of ``RegularlySamgledSignal`` with
  integer values for ``signals`` and bin-times as ``signal_base``.
  """
  def __init__(self, sample_signal, start, stop, time_units):
    self.sample_signal = sample_signal
    self.start = start
    self.stop = stop
    self.time_units = time_units
    self.hash_value = hash_value


if __name__ == '__main__':
  return True
