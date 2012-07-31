import unittest
from datajongleur.neuro.pq_based import *

def testQuantityProperties(self):
  """
  Here, arithmetic and relations are checked
  """
  #: Arithmetic
  self.assertEqual(self.a + self.b, self.c)
  self.assertEqual((self.a * self.b).getAmount(), self.b.getAmount())
  #: Relation
  self.assertNotEqual(self.a, self.d)

class TestMoment(unittest.TestCase):
  def setUp(self):
    self.a = Moment(1, 'ms')
    self.b = Moment(2, 'ms')
    self.c = Moment(3, 'ms')
    self.d = Moment(1, 'V')

  def test_quantity_properties(self):
    testQuantityProperties(self)

class TestPeriod(unittest.TestCase):
  def test_all(self):
    p1 = Period(1,2, "ms")
    p2 = Period(2,3, "ms")
    self.assertEqual(p1.length, p2.length)

class TestSampledTimeSeries(unittest.TestCase):
  def test(self):
    sts = SampledTimeSeries([1,2,3], 'mV', [1,4,7], 's')
    self.assertEqual(sts.units, "mV")

class TestSpikeTimes(unittest.TestCase):
  def test(self):
    spiketimes = SpikeTimes([1.3, 1.9, 2.5], "ms")
    self.assertEqual(spiketimes.units, "ms")

class TestRegularlySampledTimeSeries(unittest.TestCase):
  def test(self):
    rsts = RegularlySampledTimeSeries([1,2,3],"mV", 1, 5, "s")
    self.assertEqual(rsts.units, "mV")

class TestBinnedSpikes(unittest.TestCase):
  def test(self):
    bs = BinnedSpikes([5,6,2], 1.3, 5.9, "ms")
    self.assertEqual(bs.signal_base.units, 'ms')
  


if __name__=='__main__':
  unittest.main()
