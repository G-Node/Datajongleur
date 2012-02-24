import nose
import random

from datajongleur.beanbags.neuro.pq_based import *
from datajongleur.tests import session
import datajongleur.tests.i_asserts as i_asserts
import datajongleur.tests.sa_asserts as sa_asserts

numbers = []
numbers2 = []
numbers_int = []
units = []

time_units = ['s', 'ms', 'us', 'ns', 'ps']
for idx in range(4):
  numbers.append(random.random())
  numbers2.append(random.random())
  numbers_int.append(random.randint(0,10))
  units.append(random.choice(time_units))

np_numbers = np.array(numbers)
np_numbers2 = np.array(numbers2)
np_numbers_int = np.array(numbers_int)

def test_pq_based_TimePoint():
  tp = TimePoint(numbers[0], units[0])
  assert sa_asserts.sa_access(tp)
  assert tp.info == {'signal': tp.signal}

def test_pq_based_Period():
  p = Period(numbers[0:2], units[0])
  assert sa_asserts.sa_access(p)
  assert i_asserts.interval(p, start=numbers[0], stop=numbers[1]) 
  assert np.array_equal(p.info['signal'], p.signal)

def test_pq_based_sampled_time_series():
  sts = SampledTimeSeries(
      numbers,
      units[0],
      signal_base_amount = numbers2,
      signal_base_units = units[1])
  assert sa_asserts.sa_access(sts)
  assert i_asserts.interval(sts, start=np_numbers2.min(), stop=np_numbers2.max()) 
  assert i_asserts.sampled_signal(sts)
  assert i_asserts.quantity(sts, (np_numbers ** 2).max())
  assert np.array_equal(sts.info['signal_base'].magnitude, numbers2)

def test_pq_based_spike_times():
  st = SpikeTimes(numbers, units[0])
  assert sa_asserts.sa_access(st)
  assert i_asserts.interval(st, start=np_numbers.min(), stop=np_numbers.max()) 
  assert i_asserts.sampled_signal(st)
  assert i_asserts.quantity(st, (np_numbers ** 2).max())
  assert st.units == units[0]
  assert np.array_equal(st.amount, numbers)
  assert st.signal.mean() == 1

def test_pq_based_regularly_sampled_time_series():
  rsts = RegularlySampledTimeSeries(
      numbers,
      units[0],
      start=numbers2[0],
      stop=numbers2[1],
      time_units=units[1])
  assert sa_asserts.sa_access(rsts)
  assert i_asserts.interval(rsts, start=numbers2[0], stop=numbers2[1]) 
  assert i_asserts.sampled_signal(rsts)
  assert i_asserts.quantity(rsts, (np_numbers ** 2).max())

def test_pq_based_binned_spikes():
  bs = BinnedSpikes(
      numbers_int,
      start=numbers2[0],
      stop=numbers2[1],
      time_units=units[1])
  assert sa_asserts.sa_access(bs)
  assert i_asserts.interval(bs, start=numbers2[0], stop=numbers2[1]) 
  assert i_asserts.sampled_signal(bs)
  assert i_asserts.quantity(bs, (np_numbers_int ** 2).max())
