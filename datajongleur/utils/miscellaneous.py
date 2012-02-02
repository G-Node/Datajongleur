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
    repr_str = repr_str[:-3] + "]"
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

