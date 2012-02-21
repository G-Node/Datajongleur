import nose
import random
import datajongleur as dj

from datajongleur.beanbags.neuro.pq_based import *

numbers = []
units = []

session = dj.get_session()
time_units = ['s', 'ms', 'us', 'ns', 'ps']
for idx in range(2):
  numbers.append(random.random())
  units.append(random.choice(time_units))

def setup_func():
  pass

def teardown_func():
  pass

@nose.with_setup(setup_func, teardown_func)
def test_pq_based_TimePoint():
  # __new__ & __init__
  tp = TimePoint(numbers[0], units[0])
  tp.save()
  uuid = tp.uuid

  tp = TimePoint(numbers[1], units[1])
  tp.save()

  tp = TimePoint.load(uuid)
  assert tp.units == units[0]
  assert tp.amount == numbers[0]

  # info-attribute
  assert tp.info == {}

@nose.with_setup(setup_func, teardown_func)
def test_pq_based_Period():
  # __new__ & __init__
  p = Period(numbers, units[0])
  p.save()
  uuid = p.uuid

  p = Period([1, 8], units[1])
  p.save()

  # load (`newByDTO` implicitly)
  p = Period.load(uuid)
  assert p.units == units[0]
  assert np.array_equal(p.amount, numbers)

  # info-attribute
  assert p.info == {}


