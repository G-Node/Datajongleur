import unittest
from datajongleur.quantity import Quantity

class TestQuantity(unittest.TestCase):

  def setUp(self):
    self.a = Quantity(1,"mV")
    self.b = Quantity(1,"V")
    self.c = Quantity(2,"mV")
    self.d = Quantity(2,"mV")
    self.e = Quantity(3,"mV")

  def test_initialization(self):
    self.assertRaises(AssertionError, Quantity, *[1,1])
    self.assertRaises(AssertionError, Quantity, *["1","1"])
    self.assertRaises(TypeError, Quantity, 1)
    self.assertRaises(TypeError, Quantity, None)

  def test_relation(self):
    def compare(a, b):
      return a == b
    test_dict = {self.c: "1", self.d: "2"}
    self.assertRaises(AssertionError, compare, *[self.a,self.b])
    self.assertEqual(self.c,self.d)
    self.assertEqual(self.c,self.c)
    self.assertNotEqual(self.a,self.c)
    self.assertEqual(len(test_dict.items()), 1)

  def test_arithmetic(self):
    self.assertEqual(self.a + self.c, self.e)
    self.assertEqual(self.c - self.a, self.a)
    self.assertEqual(self.a * self.c, Quantity(2, "mV * mV"))
    self.assertEqual(self.e // self.c, Quantity(1, "mV / mV"))
    self.assertEqual(self.e % self.c, Quantity(1, "mV / mV"))
    self.assertEqual(divmod(self.e, self.c),
        "Not implemented.")
    self.assertEqual(self.e ** self.c,
        "Not implemented. Use ``Quantity(x**y, 'Unit')")
    self.assertEqual(self.e << self.c,
        "Not implemented. Use ``Quantity(x<<y, 'Unit')")
    self.assertEqual(self.e >> self.c,
        "Not implemented. Use ``Quantity(x>>y, 'Unit')")
    self.assertEqual(self.e & self.c,"Not implemented.")
    self.assertEqual(self.e ^ self.c,"Not implemented.")
    self.assertEqual(self.e | self.c,"Not implemented.")

if __name__=='__main__':
  unittest.main()

