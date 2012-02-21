import nose
import random
import datajongleur as dj

from datajongleur.beanbags.neuro.pq_based import *

numbers = []
numbers2 = []
units = []

session = dj.get_session()
time_units = ['s', 'ms', 'us', 'ns', 'ps']
for idx in range(4):
  numbers.append(random.random())
  numbers2.append(random.random())
  units.append(random.choice(time_units))

np_numbers = np.array(numbers)
np_numbers2 = np.array(numbers2)

def setup_func():
  pass

def teardown_func():
  pass

def info_quantity_check(iq):
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
  p = Period(numbers[0:2], units[0])
  p.save()
  uuid = p.uuid

  p = Period([1, 8], units[1])
  p.save()

  # load (`newByDTO` implicitly)
  p = Period.load(uuid)
  assert p.units == units[0]
  assert np.array_equal(p.amount, numbers[0:2])

  # info-attribute & arithmentics
  assert p.info == {}
  assert (p * p).max() == (np_numbers[0:2] ** 2).max()

@nose.with_setup(setup_func, teardown_func)
def test_pq_based_sampled_time_series():
  # __new__ & __init__
  sts = SampledTimeSeries(
      numbers,
      units[0],
      signal_base_amount = numbers2,
      signal_base_units = units[1])
  sts.save()
  uuid = sts.uuid

  # load (`newByDTO` implicitly)
  sts = SampledTimeSeries.load(uuid)
  assert sts.units == units[0]
  assert np.array_equal(sts.amount, numbers)

  # info-attribute & arithmetics
  assert np.array_equal(sts.info['signal_base'].magnitude, numbers2)
  assert (sts * sts).max() == (np_numbers ** 2).max()
  assert sts.n_sampling_points == 4
  assert sts.start == np_numbers2.min()
  assert sts.stop == np_numbers2.max()
  assert sts.signal_base.sum() == np_numbers2.sum()

@nose.with_setup(setup_func, teardown_func)
def test_pq_based_spike_times():
  # __new__ & __init__
  st = SpikeTimes(numbers, units[0])
  st.save()
  uuid = st.uuid

  # load (`newByDTO` implicitly)
  st = SpikeTimes.load(uuid)
  assert st.units == units[0]
  assert np.array_equal(st.amount, numbers)

  # info-attribute & arithmetics
  assert st.signal.mean() == 1

@nose.with_setup(setup_func, teardown_func)
def test_pq_based_regularly_sampled_time_series():
  # __new__ & __init__
  rsts = RegularlySampledTimeSeries(
      numbers,
      units[0],
      start=numbers2[0],
      stop=numbers2[1],
      time_units=units[1])
  rsts.save()
  uuid = rsts.uuid
  # load (`newByDTO` implicitly)

  # info-attribute
  pass

@nose.with_setup(setup_func, teardown_func)
def test_pq_based_binned_spikes():
  # __new__ & __init__
  # load (`newByDTO` implicitly)
  # info-attribute
  pass
