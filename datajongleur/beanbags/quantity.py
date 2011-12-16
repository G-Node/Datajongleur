import interfaces as i
import quantities as pq

###################
# QuantitiesAdapter
###################

class QuantitiesAdapter(pq.Quantity, i.Quantity):
  def __new__(cls, data, units='', dtype=None, copy=True):
    obj = pq.Quantity.__new__(cls, data, units, dtype, copy)
    obj.setflags(write=False) # Immutable
    # -----------------------------------------------------------------------
    # The following line won't be necessary after a change in 
    # the python-quantities package'
    #cls.adjust_return_types(cls, pq.Quantity) #PR: not nice to use pq.Quantity
    # -----------------------------------------------------------------------
    return obj

  def getAmount(self):
    return self.magnitude
  amount = property(getAmount)

  def getUnits(self):
    return self.dimensionality.string
  units = property(getUnits)

  def __repr__(self):
    return "QuantitiesAdapter(%s, %r)" %(self.getAmount(), self.getUnits())
  
  # ----------------------------------------------------------------------
  # The following lines won't be necessary after a fork in the
  # python-quantities packages
  #
  """
  @staticmethod
  def adjust_return_types(cls, parent_cls):

    def AdjustReturnType(func):
      def wrappedFunc(self, *args, **kwargs):
        value = func(self, *args, **kwargs)
        return QuantitiesAdapter(value.magnitude, value.dimensionality.string)
      return wrappedFunc

    def generateAdjustedFunction(parent_cls, functionName):
      @AdjustReturnType
      def foo(self, *args, **kwargs):
        function = getattr(parent_cls, functionName)
        return function(self, *args, **kwargs)
      return foo
  
    # adjusting return types of analysis functions
    functionNames = [
        'min',
        '__getitem__',
        '_get_units',
        '_set_units',
        'rescale',
        'ptp',
        'clip',
        'round',
        'trace',
        'mean',
        'var',
        'std',
        'prod',
        'cumprod',
        ]
    for functionName in functionNames:
      foo = generateAdjustedFunction(parent_cls, functionName)
      setattr(cls, functionName, foo)
  """
  # ----------------------------------------------------------------------

if __name__ == '__main__':
  a = QuantitiesAdapter([2,3], "mV")
  b = QuantitiesAdapter(1, "s")
  c = QuantitiesAdapter(2, "s")
