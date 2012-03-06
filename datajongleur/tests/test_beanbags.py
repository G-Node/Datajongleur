import nose
import quantities as pq
import numpy as np
import random

from datajongleur.beanbags.models import *
from datajongleur.tests import session

numbers = []
units =[]
time_units = ['s', 'ms', 'us', 'ns', 'ps']

for idx in range(2):
  numbers.append(random.random())
  units.append(random.choice(time_units))


def test_InfoQuantity():
  # __new__ & __init__
  a = InfoQuantity([2,3], "mV", info={'vorname': "max"}, alter=3)
  b = InfoQuantity(1, "s", name="Max", last_name="Mustermann")
  c = InfoQuantity(2, "s")
  assert InfoQuantity(c*c).units == "s**2"
  assert type(a + a) == type(a.signal)
  assert type(a.max()) == type(a.signal)
  assert type(4 * a) == type(4* a.signal) 
  assert type(a * 4) == type(a.signal * 4)
