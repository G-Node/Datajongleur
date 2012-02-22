import nose
import quantities as pq
import numpy as np
import random

from datajongleur.beanbags.neuro.pq_based import *
from datajongleur.tests import session

numbers = []
units =[]

def setup_func():
  time_units = ['s', 'ms', 'us', 'ns', 'ps']
  for idx in range(2):
    numbers.append(random.random())
    units.append(random.choice(time_units))

def teardown_func():
  pass

@nose.with_setup(setup_func, teardown_func)
def test_pq_based_InfoQuantity():
  # __new__ & __init__
  a = InfoQuantity([2,3], "mV", info={'vorname': "max"}, alter=3)
  b = InfoQuantity(1, "s", name="Max", last_name="Mustermann")
  c = InfoQuantity(2, "s")
  # Return Types (not all )
  assert a.__class__.__base__ == pq.Quantity
  #assert a.__class__.__base__ == np.ndarray
  assert type(a + a) == a.__class__.__base__
  assert type(a.max()) == a.__class__.__base__
  assert type(4 * a) == a.__class__.__base__
  assert type(a * 4) == a.__class__.__base__
  # ... is here any standardiced procedure?
