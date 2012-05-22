from datajongleur.utils.miscellaneous import NumericWithUnits
import datajongleur.beanbags.interfaces as i

class InfoQuantity(NumericWithUnits):
  def __init__(self, amount, units=None, **kwargs):
    NumericWithUnits.__init__(self, amount, units)
    self.info = kwargs2info_dict(kwargs)

  def __str_main__ (self):
    """ Representation of the inherited Quantity-part"""
    return "%r\n" % self.signal
    
  def __str_info__ (self):
    if len(self.info.keys()) == 0:
      return ""
    str_info = "Info-Attributes:\n"
    for info_attribute in self.info.iteritems():
      str_info += " %s: %r\n" %(info_attribute[0], info_attribute[1])
    return str_info
  
  def __str__(self):
    head = ">>> %s <<<\n" %(self.__class__.__name__)
    str_string = "%s\n%s" % (self.__str_main__(), self.__str_info__())
    return head + str_string[:-1]

  def __repr__(self):
    return "%s(%s, %r, info)" %(
        self.__class__.__name__,
        self.amount,
        self.units)

  @property
  def hash(self):
    return sha1(self.__str__()).hexdigest()
  
  def __hash__(self):
    return self.hash


class TimePoint(InfoQuantity, NumericWithUnits):
  def __init__(self, amount, units=None):
    NumericWithUnits.__init__(self, amount, units)

  @property
  def info(self):
    return {'signal': self.signal}

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


class Period(InfoQuantity, NumericWithUnits, i.Interval):
  def __init__(self, amount, units=None):
    NumericWithUnits.__init__(self, amount, units)
    self._start = amount[0]
    self._stop = amount[1]
    self._units = units

  def getJSON(self):
    return json.dumps({
      'start': self.start,
      'stop': self.stop,
      'units': self.units})

  def checksum_json(self):
    return checksum_json(self)

  @property
  def start(self):
    return self._start

  @property
  def stop(self):
    return self._stop

  @property
  def length(self):
    return self.start - self.stop

  def __repr__(self):
    return "%s([%s, %s], %r)" %(
        self.__class__.__name__,
        self.start,
        self.stop,
        self.units)


class SampledSignal(InfoQuantity, NumericWithUnits, i.SampledSignal, i.Interval):
  def __init__(self,
      amount,
      units,
      signal_base_amount,
      signal_base_units):
    NumericWithUnits.__init__(self, amount, units)
    self.signal_base = NumericWithUnits(signal_base_amount, signal_base_units)

  # ----- Implementing InfoQuantity ------
  @property
  def info(self):
    return {'signal_base': self.signal_base}

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
  def n_sampling_points(self):
    return Quantity(len(self), '')
  def getJSON(self):
    return json.dumps({
      'amount': self.start,
      'units': self.stop,
      'signal_base_amount': self.signal_base_amount,
      'signal_base_units': self.signal_base_units})

  # ----- Implementing Representations -------
  def checksum_json(self):
    return checksum_json(self)

  def __repr__(self):
    return "%s(%r, %r, %r, %r)" %(
        self.__class__.__name__,
        self.amount,
        self.units,
        self.signal_base.amount,
        self.signal_base.units)


class RegularlySampledSignal(InfoQuantity, NumericWithUnits, i.RegularlySampledSignal):
  def __init__(self, amount, units, period_amount, period_units):
    NumericWithUnits.__init__(self, amount, units)
    self.period = Period(period_amount, period_units)

  @property
  def start(self):
    return self.period.start

  @property
  def stop(self):
    return self.period.start

  @property
  def length(self):
    return self.period.length

  @property
  def sampling_rate(self):
    return (self.n_sample_points - 1.0) / self.length
  
  @property
  def step_size(self):
    return 1 / self.sampling_rate

  @property
  def n_sample_points(self):
    return Quantity(len(self.amount), "")
