import interfaces as i
import numpy as np
import quantities as pq

############
# Quantities
############

class QuantitiesAdapter(pq.Quantity, i.Quantity):
  def getAmount(self):
    return self.magnitude
  amount = property(getAmount)

  def getUnits(self):
    return self.dimensionality.string
  units = property(getUnits)

######
# Unum
######

def getUnumAmount(quantity):
  return quantity.asNumber()

def getUnumUnits(quantity):
  return quantity.strUnit()

def adjustUnum():
  from unum import Unum as U
  U.getAmount = getUnumAmount
  U.amount = property(getUnumAmount)
  U.getUnits = getUnumUnits
  U.units = property(getUnumUnits)


############
# EZQuantity
############

class EZQuantity(i.Quantity):
  def __init__(self, amount, units):
    self.checkParameters(amount, units)
    self._amount = amount
    self._units = units

  def checkParameters(self, amount, units):
      assert isinstance(amount, (float,int,long,complex,np.ndarray)),\
          'The first argument has to be a NUMBER (not %s).' %(
              type(amount))
      assert isinstance(units, (str, unicode)),\
          'The second argument has to be TEXT (not %s).' %(type(units))

  def set_immutable_attribute(self, value):
    raise AttributeError,\
        'Objects of type ``%s`` are immutable.' %(self.__class__.__name__)

  def getAmount(self):
    return self._amount
  amount = property(
      getAmount,
      set_immutable_attribute,
      doc="Returns the amount without unit.")

  def getUnits(self):
    return self._units
  units = property(
      getUnits,
      set_immutable_attribute,
      doc="Returns the units without amount")

  # Arithmetics
  # ===========

  def assertSameUnitAs(self, other):
    assert self.units == other.units, 'Units do not match.'

  def assertNoDivZero(self, other):
    assert self.amount != 0, 'Division by zero.'

  def __add__(self, other): # +
    self.assertSameUnitAs(other)
    return self.__class__(self.amount + other.amount, self.units)

  def __sub__(self, other): # -
    self.assertSameUnitAs(other)
    return self.__class__(self.amount - other.amount, self.units)

  def __mul__(self, other): # *
    return self.__class__(
        self.amount * other.amount, self.units + " * " + other.units)

  def __div__(self, other): # /
    return self.__class__(
        self.amount / other.amount, self.units + " / " + other.units)

  def __floordiv__(self, other): # //
    self.assertNoDivZero(other)
    return self.__class__(
        self.amount // other.amount, self.units + " / " + other.units)

  def __mod__(self, other): # %
    self.assertNoDivZero(other)
    return self.__class__(
        self.amount % other.amount, self.units + " / " + other.units)

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


