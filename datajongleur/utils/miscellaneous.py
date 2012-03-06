import numpy as np

def unspec_args2info_dict(args, kwargs):
  """
  Turns `args` and `kwargs` into one dictionary `info` by the following rule:
  
  1. If there is an argument *info*: this will be the base info-dict `info`.
     Otherwise the `info = {}`.
  2. `info` gets updated by *args*. *args* have to be of type `dict`.
  3. `info` gets updated by *kwargs*

  => Priority: kwargs > args > info

  Examples:
  def foo(*args, **kwargs):
    return unspec_args2info_dict(args, kwargs)
  print foo(
    {'vorname': 'Max'},
    {'nachname':'Mustermann'},
    info={'vorname': 'Moritz', 'alter': 100},
    nachname = 'Busch')
  >>> {'nachname': 'Busch', 'vorname': 'Max', 'alter': 100}
  """
  if kwargs.has_key('info'):
    info = kwargs.pop('info')
    assert type(info) == dict, "info has to be of type `dict`"
  else:
    info = {}
  for arg in args:
    assert type(arg) == dict, "args have to be of type `dict`"
    info.update(arg)
  for k, v in kwargs.iteritems():
    info[k] = v
  return info

def kwargs2info_dict(kwargs):
  """
  Turns `kwargs` into one dictionary `info` by the following rule:
  
  1. If there is an argument *info*: this will be the base info-dict `info`.
     Otherwise the `info = {}`.
  2. `info` gets updated by *kwargs*

  => Priority: kwargs > info

  Examples:
  def foo(**kwargs):
    return kwargs2info_dict(kwargs)
  print foo(
    info={'vorname': 'Max', 'nachname': 'Moritz', 'alter': 100},
    nachname = 'Busch')
  >>> {'nachname': 'Busch', 'vorname': 'Max', 'alter': 100}
  """
  if kwargs.has_key('info'):
    info = kwargs.pop('info')
    assert type(info) == dict, "info has to be of type `dict`"
  else:
    info = {}
  for k, v in kwargs.iteritems():
    info[k] = v
  return info

def addAttributesProxy(attr_names, object_attr):
  def deco(cls):
    for attr_name in attr_names:
      def getAttr(self, attr_name=attr_name):
        obj = getattr(self, object_attr)
        return getattr(obj, attr_name)
      def setAttr(self, value, attr_name=attr_name):
        obj = getattr(self, object_attr)
        setattr(obj, attr_name, value)
      prop = property(getAttr, setAttr)
      setattr(cls, attr_name, prop)
    return cls
  return deco

def addDictAccessByAttrs(key_names, dict_name):
  def deco(cls):
    for key_name in key_names:
      def getAttr(self, key_name=key_name):
        try:
          return getattr(self, dict_name)[key_name]
        except AttributeError, e:
          return None
        except KeyError, e:
          return None
        except TypeError, e:
          return None
      def setAttr(self, value, key_name=key_name):
        if getattr(self, dict_name) is None:
          setattr(self, dict_name, {key_name: value})
        else:
          getattr(self, dict_name)[key_name] = value
      prop = property(getAttr, setAttr)
      setattr(cls, key_name, prop)
    return cls
  return deco 

def change_return_type(result_cls):
  def decorator_func(cls):
    def AdjustReturnType(func):
      def wrappedFunc(self, *args, **kwargs):
        return func(self.view(result_cls), *args, **kwargs)
      return wrappedFunc

    def generateAdjustedFunction(functionName):
      @AdjustReturnType
      def foo(self, *args, **kwargs):
        function = getattr(cls.__base__, functionName)
        return function(self, *args, **kwargs)
      return foo
    # adjusting return types of analysis functions
    functionNames = [
        '_get_units',
        '_set_units',
        'rescale',
        'ptp',
        'clip',
        'copy',
        'compress',
        'conj',
        'cumprod',
        'cumsum',
        'diagonal',
        'dot',
        'flatten',
        'getfield',
        'round',
        'trace',
        'max',
        'mean',
        'min',
        'newbyteorder',
        'prod',
        'ravel',
        'reshape',
        'resize',
        'round',
        'std',
        'sum',
        'trace',
        'transpose',
        'var',
        '__getitem__',
        '__getslice__',
        '__abs__',
        #
        '__add__',
        '__div__',
        '__divmod__',
        '__floordiv__'
        '__mod__',
        '__mul__',
        '__pow__',
        '__sub__',
        #
        '__radd__',
        '__div__',
        '__divmod__',
        '__rfloordiv__',
        '__rmod__',
        '__rmul__',
        '__rpow__',
        '__rsub__',
        ]
    for functionName in functionNames:
      foo = generateAdjustedFunction(functionName)
      setattr(cls, functionName, foo)
    cls._arithmetic_return_type = result_cls
    return cls
  return decorator_func

class ListView(list):
  def __init__(self, raw_list, raw2new, new2raw):
    self._data = raw_list
    self.converters = {'raw2new': raw2new,
        'new2raw': new2raw}

  def __repr__(self):
    repr_list = [self.converters['raw2new'](item) for item in self._data]
    repr_str = "["
    for element in repr_list:
      repr_str += element.__repr__() + ",\n "
    if repr_str[-3:] == ",\n ":
      repr_str = repr_str[:-3]
    repr_str = repr_str + "]"
    #repr_str = repr_str[:-3] + "]"
    return repr_str

  def append(self, item):
    self._data.append(self.converters['new2raw'](item))

  def pop(self, index):
    self._data.pop(index)

  def __getitem__(self, index):
    return self.converters['raw2new'](self._data[index])

  def __setitem__(self, key, value):
    self._data.__setitem__(key, self.converters['new2raw'](value))

  def __delitem__(self, key):
    return self._data.__delitem__(key)

  def __getslice__(self, i, j):
    return ListView(self._data.__getslice__(i,j), **self.converters)

  def __contains__(self, item):
    return self._data.__contains__(self.converters['new2raw'](item))

  def __add__(self, other_list_view):
    assert self.converters == other_list_view.converters
    return ListView(
        self._data + other_list_view._data,
        **self.converters)

  def __len__(self):
    return len(self._data)

  def __iter__(self):
    return iter([self.converters['raw2new'](item) for item in self._data])

  def __eq__(self, other):
    return self._data == other._data

class NPAdapter(np.ndarray):
  def __new__(cls, signal, units):
    """
    NPAdapter is instanciated with `signal` and `units` but ignores `units`.
    """
    obj = np.array(signal)
    return obj

def adapt_numerical_functions(cls):
  def generateAdjustedFunction(functionName):
    def foo(self, *args, **kwargs):
      function = getattr(self.signal.__class__, functionName)
      return function(self.signal, *args, **kwargs)
    return foo
  functionNames = [
      '_get_units',
      '_set_units',
      'rescale',
      'ptp',
      'clip',
      'copy',
      'compress',
      'conj',
      'cumprod',
      'cumsum',
      'diagonal',
      'dot',
      'flatten',
      'getfield',
      'round',
      'trace',
      'max',
      'mean',
      'min',
      'newbyteorder',
      'prod',
      'ravel',
      'reshape',
      'resize',
      'round',
      'std',
      'sum',
      'trace',
      'transpose',
      'var',
      '__getitem__',
      '__getslice__',
      '__abs__',
      #
      '__add__',
      '__div__',
      '__divmod__',
      '__floordiv__'
      '__mod__',
      '__mul__',
      '__pow__',
      '__sub__',
      #
      '__radd__',
      '__div__',
      '__divmod__',
      '__rfloordiv__',
      '__rmod__',
      '__imul__',
      '__rmul__',
      '__rpow__',
      '__rsub__',
      ]
  for functionName in functionNames:
    foo = generateAdjustedFunction(functionName)
    setattr(cls, functionName, foo)
  return cls

@adapt_numerical_functions
class Numeric(object):
  def __init__(self, signal):
    self.set_signal(signal)

  def set_signal(self, signal):
    self.signal = signal
    if hasattr(self.signal, '_dimensionality'):
      self._dimensionality = self.signal._dimensionality
      self.dimensionality = self.signal.dimensionality

  def __array__(self):
    """
    Provide an 'array' view or copy over numeric.samples

    Parameters
    ----------
    dtype: type, optional
      If provided, passed to .signal.__array__() call

    *args to mimique numpy.ndarray.__array__ behavior which relies
    on the actual number of arguments
    """
    return self.signal
