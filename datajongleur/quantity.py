import numpy as np

class Quantity(object):
  def __init__(self, amount, units):
    self.checkParameters(amount, units)
    self._amount = amount
    self._units = units

  def checkParameters(self, amount, units):
      assert isinstance(amount, (float,int,long,complex)),\
          'The first argument has to be a NUMBER (not %s).' %(
              type(amount))
      assert isinstance(units, (str, unicode)),\
          'The second argument has to be TEXT (not %s).' %(type(units))

  def set_immutable(self, value):
    raise AttributeError,\
        'Objects of type ``%s`` are immutable.' %(self.__class__.__name__)

  def get_amount(self):
    return self._amount
  amount = property(get_amount, set_immutable, doc="Amount without unit.")

  def get_units(self):
    return self._units
  units = property(get_units, set_immutable, doc="Units without amount")

  # Arithmetics
  # ===========

  def assertSameUnitAs(self, other):
    assert self.units == other.units, 'Units do not match.'

  def assertNotDivZero(self, other):
    assert self.amount != 0, 'Division by zero.'

  def __add__(self, other): # +
    self.assertSameUnitAs(other)
    return Quantity(self.amount + other.amount, self.units)

  def __sub__(self, other): # -
    self.assertSameUnitAs(other)
    return Quantity(self.amount - other.amount, self.units)

  def __mul__(self, other): # *
    return Quantity(
        self.amount * other.amount, self.units + " * " + other.units)

  def __floordiv__(self, other): # //
    return Quantity(
        self.amount // other.amount, self.units + " / " + other.units)

  def __mod__(self, other): # %
    return Quantity(
        self.amount % other.amount, self.units + " / " + other.units)

  def __divmod__(self, other): # divmod()
    return "Not implemented."

  def __pow__(self, other): #**
    return "Not implemented. Use ``Quantity(x**y, 'Unit')"

  def __lshift__(self, other): # <<
    return "Not implemented. Use ``Quantity(x<<y, 'Unit')"

  def __rshift__(self, other): # >>
    return "Not implemented. Use ``Quantity(x>>y, 'Unit')"

  def __and__(self, other): # &
    return "Not implemented."

  def __xor__(self, other): # ^
    return "Not implemented."

  def __or__(self, other): # |
    return "Not implemented."

  def __cmp__(self, other):
    self.assertSameUnitAs(other)
    if self.amount < other.amount:
      return -1
    if self.amount == other.amount:
      return 0
    if self.amount > other.amount:
      return 1

  # Special Methods
  # ===============

  def __hash__(self):
    return hash(self.__repr__())

  def __str__(self):
    return '%s * [%s]' %(self._amount, self._units)

  def __repr__(self):
    return '%s(%r, %r)' %(self.__class__.__name__, self._amount, self._units)

if __name__=='__main__':
  a = Quantity(1, "mV")
  b = Quantity(1, "mV")
  c = Quantity(2, "mV")
