import interfaces as i
import quantities as pq
from datajongleur.beanbags.models import DTOQuantity
from datajongleur.utils.sa import passLKeyDTO, addDBAccess

###################
# Quantity
###################

@addDBAccess(DTOQuantity, 'quantity_key')
@passLKeyDTO
class Quantity(pq.Quantity, i.Quantity):
  _DTO = DTOQuantity

  def __new__(
      cls,
      amount,
      units,
      **kwargs
      ):
    dto = cls._DTO(amount=amount, units=units, **kwargs)
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

  def __array_wrap__(self, obj, context=None):
    """
    Returns a Quantity-object in case of arithmetic, e.g. ``a + b``
    """
    obj1 = pq.Quantity.__array_wrap__ (self, obj, context)
    obj2 = self.__class__(obj1.amount, obj1.units)
    return obj2

  def getDTO(self):
    if not hasattr(self, '_dto'):
      dto = self.__class__._DTO(self.amount, self.units)
      self._dto = dto
    return self._dto

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
  def __init__(self, **kwargs):
    for kw in kwargs:
      setattr(self, kw, kwargs[kw])
    

class InfoQuantity(Quantity):
  _DTO = DTOInfoQuantity
  def __new__(cls, amount, units='', dtype=None, copy=True, **kwargs):
    kwargs['dtype'] = dtype
    kwargs['copy'] = copy
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
    return obj

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


if __name__ == '__main__':
  a = Quantity([2,3], "mV")
  b = Quantity(1, "s")
  c = Quantity(2, "s")
