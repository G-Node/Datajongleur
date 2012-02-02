import numpy as np
import interfaces as i
import quantities as pq
from datajongleur.beanbags.models import DTOQuantity
from datajongleur.utils.sa import passAttrDTO, addInfoQuantityDBAccess

###################
# Quantity
###################

@addInfoQuantityDBAccess()
@passAttrDTO
class Quantity(pq.Quantity, i.Quantity):
  _DTO = DTOQuantity

  def __new__(
      cls,
      amount,
      units,
      **kwargs
      ):
    #print "in __new__"
    amount = np.array(amount)
    dto = cls._DTO(amount=amount, units=units)
    return cls.newByDTO(dto)

  @classmethod
  def newByDTO(cls, dto):
    obj = pq.Quantity.__new__(
        cls,
        dto.amount,
        dto.units).view(cls)
    obj.setflags(write=False) # Immutable
    obj._dto = dto
    return obj

  def __array_finalize__(self, obj):
    #print "in finalize"
    pq.Quantity.__array_finalize__ (self, obj)
    if hasattr(obj, '_dto'): # needed for ``copy``
      self._dto = obj._dto

  def __array_wrap__(self, obj, context=None):
    """
    Returns a Quantity-object in case of arithmetic, e.g. ``a + b``
    """
    #print "in wrap"
    obj1 = pq.Quantity.__array_wrap__ (self, obj, context)
    obj2 = Quantity(obj1.amount, obj1.units)
    return obj2

  def getDTO(self):
    if not hasattr(self, '_dto'):
      dto = self.__class__._DTO(self.amount, self.units)
      self._dto = dto
    return self._dto
  dto = property(getDTO)

  def getAmount(self):
    return self.magnitude
  amount = property(getAmount)

  def getUnits(self):
    return self.dimensionality.string
  units = property(getUnits)

  def __repr__(self):
    return "%s(%s, %r)" %(
        self.__class__.__name__,
        self.getAmount(),
        self.getUnits())


class DTOInfoQuantity(i.DTOInfoQuantity):
  """
  Not in ``models.py`` as this is too general to map it to a database.
  """
  def __init__(self, **kwargs):
    self._info_attributes = []
    for kw in kwargs:
      setattr(self, kw, kwargs[kw])
  
  def getInfoAttributes(self):
    return self._info_attributes
  def setInfoAttributes(self, values):
    raise AttributeError, "This attribute is not writable."
  info_attributes = property ( getInfoAttributes, setInfoAttributes )


class InfoQuantity(Quantity):
  _DTO = DTOInfoQuantity
  def __new__(cls, amount, units='', **kwargs):
    kwargs['amount'] = amount
    kwargs['units'] = units
    dto = cls._DTO(**kwargs)
    return cls.newByDTO(dto)

  @classmethod
  def newByDTO(cls, dto):
    obj = Quantity(
        dto.amount,
        dto.units,
        ).view(cls)
    obj._dto = dto
    obj.setflags(write=False) # Immutable
    obj._info_attributes = {}
    return obj

  def __array_prepare__(self, obj, context=None):
    res = Quantity.__array_prepare__ (self, obj, context)
    return res

  def __array_finalize__(self, obj):
    Quantity.__array_finalize__ (self, obj)
    if hasattr(obj, '_dto'): # needed for ``copy``
      self._dto = obj._dto

  def __array_wrap__(self, obj, context=None):
    """
    Returns a Quantity-object in case of arithmetic, e.g. ``a + b``
    """
    obj1 = Quantity.__array_wrap__ (self, obj, context)
    obj2 = Quantity(obj1.amount, obj1.units)
    return obj2

  def __repr_main__ (self):
    """ Representation of the inherited Quantity-part"""
    return "%r\n" % self.view(Quantity)
    return "(%s, %r)\n" % (
        #self.__class__.__name__,
        self.amount, self.units)
    
  def __repr_info__ (self):
    if len(self._info_attributes.keys()) == 0:
      return ""
    repr_info = "Info-Attributes:\n"
    for info_attribute in self._info_attributes.iteritems():
      repr_info += " %s: %r\n" %(info_attribute[0], info_attribute[1])
    return repr_info
  
  def __repr__(self):
    return "%s\n%s" % (self.__repr_main__(), self.__repr_info__())


if __name__ == '__main__':
  a = Quantity([2,3], "mV")
  b = Quantity(1, "s")
  c = Quantity(2, "s")
