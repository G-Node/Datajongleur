import numpy as np

class SampledArray(np.ndarray):
  def create_base_object(cls, input_array, sample_unit):
    """
    This class-method initializes the base-data-object. It can be changed for
    subclasses (e.g. to use quantities.Quantity instead of numpy.ndarray)
    """
    obj = np.asarray(input_array).view(cls)
    obj._sample_unit = sample_unit
    return obj

  def __new__(cls, input_array, stop=None, start=None,
      span=None, sample_rate=None, step=None, info=None,
      sample_unit=None):
    # Input array is an already formed ndarray instance
    # We first cast to be our class type
    #obj = np.asarray(input_array).view(cls)
    obj = cls.create_base_object(input_array, sample_unit)
    # add the new attribute to the created instance
    obj.info = info
    obj._sample_pts = len(input_array)
    if stop is None and start is None:
      start = 0
    #
    # getting `_stop` and `_start`
    # ----------------------------
    if stop is not None:
      obj._stop = float(stop)
      if start is not None:
        obj._start = float(start)
        return obj
      elif span is not None:
        obj._start = stop - span
        return obj
      elif sample_rate is not None:
        obj._start = float(stop) - ((obj._sample_pts-1) / float(sample_rate))
        return obj
      elif step is not None:
        obj._start = float(stop) - ((obj._sample_pts-1) * float(sample_rate))
        return obj
      else:
        # As there are not sufficient parameters, start is set to default = 0
        obj._start = 0.
        return obj
    elif start is not None:
      obj._start = float(start)
      if span is not None:
        obj._stop = start + span
        counter -=1
        return obj
      elif sample_rate is not None:
        obj._stop = start + ((obj._sample_pts-1) / float(sample_rate))
        return obj
      elif step is not None:
        obj._stop = float(start) + ((obj._sample_pts-1) * float(step))
        return obj
      else:
        obj._stop = start + len(input_array) - 1
      obj._start = float(obj._start)
      obj._stop = float(obj._stop)
    
    # Finally, we must return the newly created object:
    return obj

  def __array_finalize__(self, obj):
    # see InfoArray.__array_finalize__ for comments
    if obj is None: return
    self.info = getattr(obj, 'info', None)

  # -------------------------
  # define properties -------
  # -------------------------

  # Create property: span
  def get_span(self):
    return self._stop - self._start
  def set_span(self, value):
    print "Just changable at initialization!"
    #self._stop = self._start + value 
  span = property(fget=get_span, fset=set_span,
      doc='span := stop - start')

  # Create property: start
  def get_start(self):
    return self._start
  def set_start(self, value):
    diff = self._start - value
    self._start = value
    self._stop = self._stop - diff
    print "also ``stop`` was changed to %s" %(self._stop)
  start = property(fget=get_start, fset=set_start, doc='`start`-parameter')

  # Create property: stop
  def get_stop(self):
    return self._stop
  def set_stop(self, value):
    diff = self._start - value
    print diff
    self._stop = value
    self._start = self._start + diff
    print "also ``start`` was changed to %s" %(self._start)
  stop = property(fget=get_stop, fset=set_stop, doc='`stop`-parameter')

  # Create property: sample_pts
  def get_sample_pts(self):
    return self._sample_pts
  def set_sample_pts(self, value):
    print "not possible"
  sample_pts = property(fget=get_sample_pts, fset=set_sample_pts,
      doc='number of samples')
  
  # Create property: sample_rate
  def get_sampling_rate(self):
    return float(self._sample_pts - 1) / (self._stop - self._start) 
  def set_sampling_rate(self, value):
    """
    Unit: Hertz [Hz]
    """
    #self._stop = self._start + (self._stop - self._start) * 1.0/value
    self._stop = self._start + (self._sample_pts-1)/ float(value)
  sampling_rate = property(fget=get_sampling_rate, fset=set_sampling_rate,
      doc='sample_rate := 1 / step')

  # Create property: step
  def get_step(self):
    return (self._stop - self._start) / (self._sample_pts - 1)
  def set_step(self, value):
    """
    Unit: Second [s]
    """
    self.set_sample_rate(1.0 / value)
  step = property(fget=get_step, fset=set_step, 
      doc='difference of two adjacend samples')

  # Create property: sampling_base
  def get_sampling_base(self):
    return np.linspace(self._start, self._stop, self._sample_pts)
  def set_sampling_base(self, value):
    print "not specified"
  sampling_base = property(
      fget=get_sampling_base,
      fset=set_sampling_base,
      doc='sampling basis')

  # ----------------------
  # setting aliases-------
  # ----------------------
  sb = sampling_base
  sr = sampling_rate
  sample_rate = sampling_rate

  # ----------------------
  # define class-method---
  # ----------------------
  create_base_object = classmethod(create_base_object)


if __name__ == "__main__":
  a = np.array([1,2,3,4,5,6.8])
  b = SampledArray(a)
  c = SampledArray(a, stop=10)
