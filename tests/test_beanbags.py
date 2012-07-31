# -*- coding: utf-8 -*-
import nose
import quantities as pq
import numpy as np
import random

from datajongleur.beanbags.models import *
from datajongleur.beanbags.nwu import NumericWithUnits
from tests import *

import tests.i_asserts as i_asserts
import tests.sa_asserts as sa_asserts


def test_NumericWithUnits():
    num = NumericWithUnits(pq.Quantity([1, 2, 3], 'mV'))
    num2 = NumericWithUnits(np.array([1, 2, 3]), 'mV')
    q = pq.Quantity([2, 3, 4], 'mV')
    n = np.array([3, 4, 5])
    assert type(num * num) == type(num.signal * num.signal)
    assert type(n * num) == type(n * num.signal)
    assert type(q + num) == type(q + num.signal)
    assert type(q * num) == type(q * num.signal)
    nose.tools.assert_raises(ValueError, sum, *(n, num))
    assert (num * num).dimensionality.string\
        == (num.signal * num.signal).dimensionality.string

def test_Tag():
    tp = TimePoint(numbers[0], units[0])
    p = Period(numbers[0:2], units[0])
    tp.tags.append('blau')
    tp.tags.append(u'grün')
    p.tags.append('blau')
    tp.save()
    p.save()
    t = Tag.query.filter_by(name='blau').one()
    return t

def test_InfoQuantity():
    a = InfoQuantity([2, 3], "mV", info={'vorname': "max"}, alter=3)
    b = InfoQuantity(1, "s", name="Max", last_name="Mustermann")
    c = InfoQuantity(2, "s")
    print "----", c * c, type(c * c)
    assert type(a + a) == type(a.signal)
    assert type(a.max()) == type(a.signal)
    assert type(4 * a) == type(4 * a.signal)
    assert type(a * 4) == type(a.signal * 4)
    nose.tools.assert_raises(AssertionError, InfoQuantity, *(c * c, 's'))
    nose.tools.assert_raises(AssertionError, InfoQuantity, *(c, 's**2'))


def test_TimePoint():
    tp = TimePoint(numbers[0], units[0])
    assert sa_asserts.sa_access(tp)
    assert tp.info == {}


def test_Period():
    p = Period(numbers[0:2], units[0])
    assert sa_asserts.sa_access(p)
    assert i_asserts.interval(p, start=numbers[0], stop=numbers[1])
    assert np.array_equal(p.info['start'], p.start)
    assert np.array_equal(p.info['stop'], p.stop)
    assert np.array_equal(p.info['length'], p.length)


def test_SimpleSampledSignal():
    sts = SimpleSampledSignal(
        numbers,
        units[0],
        signal_base_amount=numbers2,
        signal_base_units=units[1])
    assert sa_asserts.sa_access(sts)
    assert i_asserts.sampled_signal(sts)
    assert i_asserts.quantity(sts, (np_numbers ** 2).max())
    assert np.array_equal(sts.info['signal_base'].amount, numbers2)


def test_RegularlySimpleSampledSignal():
    rsts = RegularlySimpleSimpleSampledSignal(
        numbers,
        units[0],
        [numbers2[0], numbers2[1]],
        units[1])
    assert sa_asserts.sa_access(rsts)
    assert i_asserts.interval(rsts, start=numbers2[0], stop=numbers2[1])
    assert i_asserts.sampled_signal(rsts)
    assert i_asserts.quantity(rsts, (np_numbers ** 2).max())

"""
@nose.tools.raises(AssertionError)
def test_raises_assert_errors():
  c = InfoQuantity(2, "s")
  InfoQuantity(c*c, 's')
"""

if __name__ == "__main__":
    t = test_Tag()