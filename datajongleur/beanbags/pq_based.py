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


if __name__ == '__main__':
  a = InfoQuantity([2,3], "mV", info={'vorname': "max"}, alter=3)
  b = InfoQuantity(1, "s", name="Max", last_name="Mustermann")
  c = InfoQuantity(2, "s")
