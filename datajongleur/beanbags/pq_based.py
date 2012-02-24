import numpy as np
import quantities as pq
from hashlib import sha1

import interfaces as i
from datajongleur.beanbags.models import DTOQuantity, DTOInfoQuantity
from datajongleur.utils.sa import addInfoQuantityDBAccess, dtoAttrs2Info
from datajongleur.utils.miscellaneous import *

###################
# Quantity
###################

@addInfoQuantityDBAccess
@addAttributesProxy(['uuid'], '_dto')
@change_return_type(pq.Quantity)
class InfoQuantity(pq.Quantity, i.Quantity):
  """
  Note: InfoQuantities are immutable. In order to change values, you need to
  work with a `copy()` and apply `setflags(write=True)`.
  """
  _DTO = DTOInfoQuantity

  def __new__(cls, data, units='', dtype=None, copy=True,
      *args, **kwargs):
    obj = cls.__base__.__new__(
        cls.__base__,
        data,
        units=units,
        dtype=dtype,
        copy=copy).view(cls)
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

  def __str_main__ (self):
    """ Representation of the inherited Quantity-part"""
    return "%r\n" % self.view(pq.Quantity)
    
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


if __name__ == '__main__':
  a = InfoQuantity([2,3], "mV", info={'vorname': "max"}, alter=3)
  b = InfoQuantity(1, "s", name="Max", last_name="Mustermann")
  c = InfoQuantity(2, "s")
