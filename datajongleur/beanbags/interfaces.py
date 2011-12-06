class Value(object):
  def throwSetImmutableAttributeError(self, value):
    raise AttributeError, "Value object is not writable"
  def __hash__(self):
    raise NotImplementedError
  def __str__(self):
    raise NotImplementedError
  def __repr__(self):
    raise NotImplementedError
  def __cmp__(self, other):
    raise NotImplementedError


class Quantity(Value):
  #def __init__(self, amount, units):
  #  raise NotImplementedError

  # Required methods by general ``quantity``
  # ----------------------------------------
  def getAmount(self):
    raise NotImplementedError
  def getUnits(self):
    raise NotImplementedError
  # Arithmetics:
  def add(self, other): # +
    raise NotImplementedError
  def subtract(self, other): # -
    raise NotImplementedError
  def multiply(self, other): # *
    raise NotImplementedError
  def devide(self, other):
    raise NotImplementedError
  def floordiv(self, other): # //
    raise NotImplementedError
  def mod(self, other): # %
    raise NotImplementedError
  def divmod(self, other): # divmod
    raise NotImplementedError
  def pow(self, other): #**
    raise NotImplementedError
  def lshift(self, other): # <<
    raise NotImplementedError
  def rshift(self, other): # >>
    raise NotImplementedError
  def logic_and(self, other): # &
    raise NotImplementedError
  def logic_xor(self, other): # ^
    raise NotImplementedError
  def cmp(self, other):
    raise NotImplementedError
  
  # Python specific method-aliases:
  def __add__(self, other): # +
    return self.add(self, other)
  def __sub__(self, other): # -
    return self.subtract(self, other)
  def __mul__(self, other): # *
    return self.multiply(self, other)
  def __div__(self, other): # /
    return self.devide(self, other)
  def __truediv__(self, other): # /
    return self.devide(self, other)
  def __floordiv__(self, other): # //
    return self.floordiv(self, other)
  def __mod__(self, other): # %
    return self.mod(self, other)
  def __divmod__(self, other): # divmod
    return self.divmod(self, other)
  def __pow__(self, other): #**
    return self.pow(self, other)
  def __lshift__(self, other): # <<
    return self.lshift(self, other)
  def __rshift__(self, other): # >>
    return self.rshift(self, other)
  def __and__(self, other): # &
    return self.logic_and(self, other)
  def __xor__(self, other): # ^
    return self._logic_xor(self, other)
  def __cmp__(self, other):
    return self.cmp(self, other)


class Interval(Value):
  def getStart(self):
    raise NotImplementedError
  def getStop(self):
    raise NotImplementedError
  def getLength(self):
    raise NotImplementedError


class SampledSignal(Quantity):
  def getSignal(self):
    raise NotImplementedError
  def getSignalBase(self):
    raise NotImplementedError
  def getNSamplingPoints(self):
    raise NotImplementedError


class RegularlySampledSignal(SampledSignal):
  def getSamplingRate(self):
    raise NotImplementedError
  def getStepSize(self):
    raise NotImplementedError

class DTO(object):
  def getJSON(self):
    """
    To facilitate data-exchange.
    """
    raise NotImplementedError
  def getDict(self):
    raise NotImplementedError
  def getXML(self):
    """
    To facilitate data-exchange.
    """
    raise NotImplementedError
  def getChecksum(self):
    raise NotImplementedError
  def getLKey(self):
    raise NotImplementedError
