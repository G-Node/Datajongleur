from datajongleur.utils.miscellaneous import adapt_numerical_functions
from datajongleur.utils.miscellaneous import kwargs2info_dict
from datetime import datetime as dt
from uuid import uuid4
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
      self._units = amount.units
    elif type(amount)==Quantity: # Quantity - if installed, otherwise None
      assert units==None or units==amount.dimensionality.string
      self._amount= amount.view(np.ndarray)
      self._units = amount.dimensionality.string
    else:
      self._amount = np.array(amount)
      self._units = units
    if type(self.signal) == Quantity:
      self._dimensionality = self.signal._dimensionality
      self.dimensionality = self.signal.dimensionality
  
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

  def __str__(self):
    return self.signal.__str__()

  def __repr__(self):
    return self.signal.__repr__()


class Identity(object):
  def __init__(self):
    now = dt.now()
    self.ctime = now
    self.mtime = now
    self.uuid = uuid4()


class InfoQuantity(Identity, NumericWithUnits):
  def init_signal(self, amount, units):
    NumericWithUnits.__init__(self, amount, units)

  def __init__(self, amount, units=None, **kwargs):
    print 1
    Identity.__init__(self)
    self.init_signal(amount, units)
    self._info = kwargs2info_dict(kwargs)
    self.check_info()

  def check_info(self):
    """
    Used by inheritors.
    """
    pass

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
  
  @property
  def info(self):
    res = {'signal': self.signal}
    res.update(self._info)
    return res
