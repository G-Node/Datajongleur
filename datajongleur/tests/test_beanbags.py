import nose
import quantities as pq
import numpy as np
import random

from datajongleur.core.models import *
from datajongleur.tests.utils import session
from datajongleur.core.beanbags import NumericWithUnits

numbers = []
units =[]
time_units = ['s', 'ms', 'us', 'ns', 'ps']

for idx in range(2):
  numbers.append(random.random())
  units.append(random.choice(time_units))

def test_NumericWithUnits():
  num = NumericWithUnits(pq.Quantity([1,2,3], 'mV'))
  num2 = NumericWithUnits(np.array([1,2,3]), 'mV')
  q = pq.Quantity([2,3,4], 'mV')
  n = np.array([3,4,5])
  assert type(num * num) == type(num.signal * num.signal)
  assert type(n * num) == type(n * num.signal)
  assert type(q + num) == type(q + num.signal)
  assert type(q * num) == type(q * num.signal)
  nose.tools.assert_raises(ValueError, sum, *(n, num))
  assert (num*num).dimensionality.string\
      == (num.signal*num.signal).dimensionality.string

def test_InfoQuantity():
  # __new__ & __init__
  a = InfoQuantity([2,3], "mV", info={'vorname': "max"}, alter=3)
  b = InfoQuantity(1, "s", name="Max", last_name="Mustermann")
  c = InfoQuantity(2, "s")
  print "----", c*c, type(c*c)
  assert type(a + a) == type(a.signal)
  assert type(a.max()) == type(a.signal)
  assert type(4 * a) == type(4* a.signal) 
  assert type(a * 4) == type(a.signal * 4)
  nose.tools.assert_raises(AssertionError, InfoQuantity, *(c*c, 's'))
  nose.tools.assert_raises(AssertionError, InfoQuantity, *(c, 's**2'))

"""
@nose.tools.raises(AssertionError)
def test_raises_assert_errors():
  c = InfoQuantity(2, "s")
  InfoQuantity(c*c, 's')
"""
