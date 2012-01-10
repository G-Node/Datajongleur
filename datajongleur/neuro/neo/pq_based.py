class Segment(object):

  def add_analog_signal(self, asig):
    try:
      self._dtos_analog_signal.append(asig._dto_analog_signal)
      asig._dto_analog_signal._dto_regularly_sampled_time_series =\
          asig._dto_regularly_sampled_time_series
    except exc.SQLAlchemyError, e:
      print "Problem: %s" % e[0]

  def add_event(self, event):
    try:
      self._dtos_event.append(event._dto_event)
      event._dto_event._dto_time_point =\
          event._dto_time_point
    except exc.SQLAlchemyError, e:
      print "Problem: %s" % e[0]

  def get_analog_signal(self, idx):
    dto_asig = self._dtos_analog_signal[idx]
    asig = AnalogSignal.newByDTO(dto_asig._dto_regularly_sampled_time_series)
    asig._dto_analog_signal = dto_asig
    return asig

  def get_list_of_analog_signals(self):
    list_of_anasigs = []
    for idx, anasig in enumerate(self._dtos_analog_signal):
      list_of_anasigs.append(self.get_analog_signal(idx))
    return list_of_anasigs

  def info(self):
    print self._dtos_analog_signal


