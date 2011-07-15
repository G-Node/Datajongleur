import quantities as pq

class pqSampledArray(pq.Quantity, SampledArray):
  def create_base_object(cls, input_array, sample_unit):
    """
    This class-method replaces the parent class method in order to use
    quantities.Quantity instead of numpy.ndarray)
    """
    obj = pq.Quantity(input_array, sample_unit).view(cls)
    return obj

  def __new__(cls, input_array, t_unit='s',
      stop=None, start=None, span=None, sample_rate=None, step=None,
      info=None, sample_unit='dimensionless'):
    #: Call the parent class constructor
    obj = SampledArray.__new__(cls, input_array, stop, start,
      span, sample_rate, step, info, sample_unit)
    #: adding units
    #obj.units = sample_unit
    obj._start = pq.Quantity(obj._start, t_unit)
    obj._stop = pq.Quantity(obj._stop, t_unit)
    return obj

  create_base_object = classmethod(create_base_object)

