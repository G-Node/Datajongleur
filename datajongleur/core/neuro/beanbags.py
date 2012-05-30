from datajongleur.core.beanbags import Identity
from datajongleur.core.beanbags import NumericWithUnits
import datajongleur.core.interfaces as i
import datajongleur.core.beanbags as core_bb
import numpy as np
import json

class TimePoint(core_bb.InfoQuantity):
  def check_info(self):
    pass
    #self._info = {}

  def getDict(self):
    return {
        'amount': self.amount,
        'units': self.units}

  def getJSON(self):
    return json.dumps(self.getDict())

  def checksum_json(self):
    return checksum_json(self)

  def getXML(self):
    from datajongleur.tools.xml_jongleur import dict2xml
    xml = dict2xml(d)
    xml.display()
    return xml

  def __repr__(self):
    return "%s(%s, %r)" %(
        self.__class__.__name__,
        self.amount,
        self.units)

  @property
  def info(self):
    return {'signal': self.signal}


class Interval(core_bb.InfoQuantity, i.Interval):
  def check_info(self):
    self._start = self.start
    self._stop = self.stop

  @property
  def start(self):
    return self.signal[0]

  @property
  def stop(self):
    return self.signal[1]

  @property
  def length(self):
    return self.signal[1] - self.signal[0]

  def getJSON(self):
    return json.dumps({
      'start': self.start,
      'stop': self.stop,
      'units': self.units})

  def checksum_json(self):
    return checksum_json(self)


class SampledTimeSeries(core_bb.InfoQuantity, i.SampledSignal, i.Interval):
  def __init__(self,
      amount,
      units,
      signal_base_amount,
      signal_base_units):
    signal_base = NumericWithUnits(signal_base_amount, signal_base_units)
    core_bb.InfoQuantity.__init__(self, amount, units, signal_base=signal_base)

  def getJSON(self):
    return json.dumps({
      'amount': self.start,
      'units': self.stop,
      'signal_base_amount': self.signal_base_amount,
      'signal_base_units': self.signal_base_units})

  def checksum_json(self):
    return checksum_json(self)


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
  def signal_base(self):
    return self.info['signal_base']

  @property
  def n_sampling_points(self):
    return Quantity(len(self), '')


class SpikeTimes(SampledTimeSeries):
  def __init__(self,
      amount,
      units):
    signal_base = NumericWithUnits(signal_base_amount, signal_base_units)

  @property
  def info(self):
    signal = Quantity(np.ones(len(self), dtype=bool))
    signal_base = self.signal
    return {
        'signal': signal,
        'signal_base': signal_base}
 
