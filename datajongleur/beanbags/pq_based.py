import numpy as np
import quantities as pq
from hashlib import sha1

import interfaces as i
from datajongleur.beanbags.models import DTOQuantity, DTOInfoQuantity
from datajongleur.utils.sa import addInfoQuantityDBAccess
from datajongleur.utils.miscellaneous import kwargs2info_dict
from datajongleur.utils.miscellaneous import change_return_type


###################
# Quantity
###################

@addInfoQuantityDBAccess
@change_return_type(pq.Quantity)
class InfoQuantity(pq.Quantity, i.Quantity):
  """
  Note: InfoQuantities are immutable. In order to change values, you need to
  work with a `copy()` and apply `setflags(write=True)`.
  """
  _DTO = DTOInfoQuantity

  def __new__(cls, data, units='', dtype=None, copy=True,
      *args, **kwargs):
    obj = pq.Quantity.__new__(cls, data, units=units, dtype=dtype, copy=copy)
    obj.setflags(write=False) # Immutable
    return obj

  def __init__(self, data, units='', dtype=None, copy=True, **kwargs):
    info = kwargs2info_dict(kwargs)
    self._dto = self._DTO(
        amount=self.magnitude,
        units=self.dimensionality.string,
        **info)
    
  @classmethod
  def newByDTO(cls, dto):
    obj = cls.__new__(
        cls,
        dto.amount,
        dto.units,
        )
    obj._dto = dto
    return obj
  
  def getDTO(self):
    return self._dto

  @property
  def info(self):
    return self._dto.info

  @info.setter
  def info(self, value):
    assert type(value) == dict, "TypeError: `value` has to be of type `dict`"
    self._dto.info = value

  @property
  def amount(self):
    return self.magnitude

  @property
  def units(self):
    return self.dimensionality.string

  def __repr_main__ (self):
    """ Representation of the inherited Quantity-part"""
    return "%r\n" % self.view(pq.Quantity)
    
  def __repr_info__ (self):
    if len(self.info.keys()) == 0:
      return ""
    repr_info = "Info-Attributes:\n"
    for info_attribute in self.info.iteritems():
      repr_info += " %s: %r\n" %(info_attribute[0], info_attribute[1])
    return repr_info
  
  def __repr__(self):
    head = ">>> %s <<<\n" %(self.__class__.__name__)
    repr_string = "%s\n%s" % (self.__repr_main__(), self.__repr_info__())
    return head + repr_string

  @property
  def hash(self):
    return sha1(self.__repr__()).hexdigest()
  
  def __hash__(self):
    return self.hash


if __name__ == '__main__':
  a = InfoQuantity([2,3], "mV", info={'vorname': "max"}, alter=3)
  b = InfoQuantity(1, "s", name="Max", last_name="Mustermann")
  c = InfoQuantity(2, "s")
