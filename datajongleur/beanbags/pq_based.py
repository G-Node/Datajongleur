import numpy as np
import interfaces as i
import quantities as pq
from datajongleur.beanbags.models import DTOQuantity, DTOInfoQuantity
from datajongleur.utils.sa import passAttrDTO, addInfoQuantityDBAccess

###################
# Quantity
###################

@addInfoQuantityDBAccess()
@passAttrDTO
class Quantity(pq.Quantity, i.Quantity):
  _BBDTO = DTOQuantity

  def __new__(
      cls,
      amount,
      units,
      **kwargs
      ):
    amount = np.array(amount)
    bb_dto = cls._BBDTO(amount=amount, units=units)
    return cls.newByDTO(bb_dto)

  @classmethod
  def newByDTO(cls, bb_dto):
    obj = pq.Quantity.__new__(
        cls,
        bb_dto.amount,
        bb_dto.units).view(cls)
    obj.setflags(write=False) # Immutable
    obj._bb_dto = bb_dto
    return obj

  def __array_finalize__(self, obj):
    pq.Quantity.__array_finalize__ (self, obj)
    if hasattr(obj, '_bb_dto'):
      self._bb_dto = obj._bb_dto
      if hasattr(obj._bb_dto, 'info_attributes'):
        # PR: durty hack --> needs to be changed
        if obj._bb_dto.info_attributes == {'copy': False}:
          obj._bb_dto.info_attributes = {}

  def __array_wrap__(self, obj, context=None):
    """
    Returns a Quantity-object in case of arithmetic, e.g. ``a + b``
    """
    print "in wrap"
    obj1 = pq.Quantity.__array_wrap__ (self, obj, context)
    obj2 = Quantity(obj1.amount, obj1.units)
    return obj2

  def getDTO(self):
    if not hasattr(self, '_bb_dto'):
      bb_dto = self.__class__._BBDTO(self.amount, self.units)
      self._bb_dto = bb_dto
    return self._bb_dto
  "bb_dto = property(getDTO)"

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


class InfoQuantity(Quantity):
  _BBDTO = DTOInfoQuantity
  def __new__(cls, amount, units='', **kwargs):
    kwargs['amount'] = amount
    kwargs['units'] = units
    bb_dto = cls._BBDTO(**kwargs)
    return cls.newByDTO(bb_dto)

  @classmethod
  def newByDTO(cls, bb_dto):
    obj = Quantity(
        bb_dto.amount,
        bb_dto.units,
        ).view(cls)
    obj._bb_dto = bb_dto
    obj.setflags(write=False) # Immutable
    return obj

  @property
  def info_attributes(self):
    return self._bb_dto.info_attributes

  @info_attributes.setter
  def info_attributes(self, value):
    assert type(value) == dict, "TypeError: `value` has to be of type `dict`"
    self._bb_dto.info_attributes = value

  def __array_prepare__(self, obj, context=None):
    print "---------------------------------------------- preparing"
    res = Quantity.__array_prepare__ (self, obj, context)
    return res

  def __array_wrap__(self, obj, context=None):
    """
    Returns a Quantity-object in case of arithmetic, e.g. ``a + b``
    """
    print "wrapping --> InfoQuantity"
    obj1 = Quantity.__array_wrap__ (self, obj, context)
    obj2 = Quantity(obj1.amount, obj1.units)
    return obj2

  def __repr_main__ (self):
    """ Representation of the inherited Quantity-part"""
    return "%r\n" % self.view(Quantity)
    
  def __repr_info__ (self):
    if len(self.info_attributes.keys()) == 0:
      return ""
    repr_info = "Info-Attributes:\n"
    for info_attribute in self.info_attributes.iteritems():
      repr_info += " %s: %r\n" %(info_attribute[0], info_attribute[1])
    return repr_info
  
  def __repr__(self):
    head = ">>> %s <<<\n" %(self.__class__.__name__)
    repr_string = "%s\n%s" % (self.__repr_main__(), self.__repr_info__())
    return head + repr_string


if __name__ == '__main__':
  a = Quantity([2,3], "mV")
  b = Quantity(1, "s")
  c = Quantity(2, "s")
