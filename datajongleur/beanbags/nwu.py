from datajongleur.utils.miscellaneous import adapt_numerical_functions
from datajongleur.utils.miscellaneous import kwargs2info_dict
import datajongleur.beanbags.interfaces as i

import numpy as np
try:
  from quantities import Quantity
except ImportError:
  Quantity = None

@adapt_numerical_functions
class NumericWithUnits(object):
  def __init__(self, amount, units=None):
    if type(amount)==type(self):
      assert units==None or units==amount.units
      self._amount = amount.amount
      self._units = unicode(amount.units)
    elif type(amount)==Quantity: # Quantity - if installed, otherwise None
      assert units==None or units==amount.dimensionality.string
      self._amount= amount.view(np.ndarray)
      self._units = unicode(amount.dimensionality.string)
    else:
      self._amount = np.array(amount)
      self._units = unicode(units)
    if type(self.signal) == Quantity:
      self._dimensionality = self.signal._dimensionality
      self.dimensionality = self.signal.dimensionality
    self._amount.setflags(write='False')
  
  @property
  def signal(self):
    if Quantity:
      return Quantity(self._amount, self._units)
    else:
      return self._amount

  @property
  def amount(self):
    return self._amount

  @property
  def units(self):
    return self._units

  def __repr__(self):
    return "%s(%r, %r)" %(
        self.__class__.__name__,
        self.amount,
        self.units)

  def __array__(self):
    """
    Provide an 'array' view or copy over numeric.samples

    Parameters
    ----------
    dtype: type, optional
      If provided, passed to .signal.__array__() call

    *args to mimique numpy.ndarray.__array__ behavior which relies
    on the actual number of arguments
    """
    return self.signal

  def __array_wrap__(self, out_arr, context=None):
    my_type = type(context[0](self.signal,out_arr))
    if hasattr(my_type, 'dimensionality'):
      return my_type(out_arr, self.units)
    else:
      return out_arr


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
        return {}
        #return {'signal': self.signal}

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

    @property
    def info(self):
        return {'start': self.start,
                'stop': self.stop,
                'length': self.length}

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
        return self.stop - self.start

    def __repr__(self):
        return "%s([%s, %s], %r)" %(
            self.__class__.__name__,
            self.start,
            self.stop,
            self.units)


class SampledSignal(InfoQuantity, NumericWithUnits,
    i.SampledSignal):
    def __init__(self, amount, units, signal_base_amount, signal_base_units):
        NumericWithUnits.__init__(self, amount, units)
        self.signal_base = NumericWithUnits(
            signal_base_amount, signal_base_units)

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
        return len(self)
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


class RegularlySampledSignal(InfoQuantity, NumericWithUnits,
    i.RegularlySampledSignal):
    def __init__(self, amount, units, period_amount, period_units):
        NumericWithUnits.__init__(self, amount, unicode(units))
        self.period = Period(period_amount, unicode(period_units))

    @property
    def start(self):
        return self.period.start

    @property
    def stop(self):
        return self.period.stop

    @property
    def length(self):
        return self.period.length
    
    @property
    def n_sampling_points(self):
        return len(self.amount)

    @property
    def sampling_rate(self):
        return (self.n_sampling_points - 1.0) / self.length
    
    @property
    def step_size(self):
        return 1 / self.sampling_rate

    @property
    def signal_base(self):
        import numpy as np
        return NumericWithUnits(
            np.linspace(self.start, self.stop, self.n_sampling_points),
            self.period.units)
    
    @property  
    def checksum_json(self):
        return checksum_json(self)
