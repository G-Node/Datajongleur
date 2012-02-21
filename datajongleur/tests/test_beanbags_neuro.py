import nose
import random
import datajongleur as dj

from datajongleur.beanbags.neuro.pq_based import *

numbers = []
units =[]

def setup_func():
  session = dj.get_session()
  time_units = ['s', 'ms', 'us', 'ns', 'ps']
  for idx in range(2):
    numbers.append(random.random())
    units.append(random.choice(time_units))

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
