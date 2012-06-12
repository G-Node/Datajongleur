import nose
import quantities as pq
import numpy as np
import random

from datajongleur.beanbags.models import *
from datajongleur.beanbags.neuro.models import *

import datajongleur.tests.i_asserts as i_asserts
import datajongleur.tests.sa_asserts as sa_asserts

#from datajongleur.tests import session

numbers = []
numbers2 = []
numbers_int = []
units = []
time_units = ['s', 'ms', 'us', 'ns', 'ps']

for idx in range(4):
    numbers.append(random.random())
    numbers2.append(random.random())
    numbers_int.append(random.randint(0, 10))
    units.append(random.choice(time_units))

np_numbers = np.array(numbers)
np_numbers2 = np.array(numbers2)
np_numbers_int = np.array(numbers_int)

def test_SpikeTimes():
    st = SpikeTimes(numbers, units[0])
    assert sa_asserts.sa_access(st)
    assert i_asserts.interval(st, start=np_numbers.min(), stop=np_numbers.max())
    assert i_asserts.sampled_signal(st)
    assert i_asserts.quantity(st.signal_base, (np_numbers ** 2).max())
    assert st.signal_base.units == units[0]
    assert np.array_equal(st.signal_base.amount, numbers)
    assert st.signal.mean() == 1


def test_BinnedSpikes():
    bs = BinnedSpikes(
        numbers_int,
        [numbers2[0], numbers2[1]],
        time_units[1])
    assert sa_asserts.sa_access(bs)
    assert i_asserts.interval(bs, start=numbers2[0], stop=numbers2[1])
    assert i_asserts.sampled_signal(bs)
    assert i_asserts.quantity(bs, (np_numbers_int ** 2).max())
