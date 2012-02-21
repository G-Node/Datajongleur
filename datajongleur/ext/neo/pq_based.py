from datajongleur.ext.neuro.neo.models import *
from datajongleur.ext.neuro.pq_based import *
from datajongleur.utils.miscellaneous import *

Block = addDictAccessByAttrs(['file_origin', 'brain_region'], 'badges')(Block)
Segment = addDictAccessByAttrs(['file_origin'], 'badges')(Segment)
RecordingChannel = addDictAccessByAttrs(
    ['file_origin'], 'badges')(RecordingChannel)
RecordingChannelGroup = addDictAccessByAttrs(
    ['file_origin'],'badges')(RecordingChannelGroup)
Unit = addDictAccessByAttrs(
    ['file_origin'],'badges')(Unit)

@addDictAccessByAttrs(['file_origin'], 'badges')
@addAttributesProxy(['name', 'description', 'flag', 'badges'], '_dto_analog_signal')
@addAttributesProxy(
    ['uuid', 'segment', 'recording_channel'], '_dto_analog_signal')
class AnalogSignal(RegularlySampledTimeSeries):
  def __init__(self, *args, **kwargs):
    # real initialization takes place at `RegularlySampledTimeSeries.__newByDTO__(...)`
    self._dto_analog_signal = DTOAnalogSignal()
    self.__init_finalize__()

  def __init_finalize__(self):
    self._dto_analog_signal.dto_regularly_sampled_time_series = \
        self._dto

  @classmethod
  def newByDTOAnalogSignal(cls, dto):
    obj = cls.newByDTO(dto.dto_regularly_sampled_time_series)
    obj._dto_analog_signal = dto
    obj.__init_finalize__()
    return obj
 
  def getBeanbag(self):
    return self.__class__.__base__.newByDTO(
        self._dto)

  def getDTOAnalogSignal(self):
    return self._dto_analog_signal

@addDictAccessByAttrs(['file_origin'], 'badges')
@addAttributesProxy(['name', 'description', 'flag', 'badges'], '_dto_spike_times')
@addAttributesProxy(
    ['uuid', 'segment', 'unit'], '_dto_spike_times')
class SpikeTrain(SpikeTimes):
  def __init__(self, *args, **kwargs):
    # real initialization takes place at `RegularlySampledTimeSeries.__newByDTO__(...)`
    self._dto_spike_times = DTOSpikeTimes()
    self.__init_finalize__()

  def __init_finalize__(self):
    self._dto_spike_train.dto_spike_times = \
        self._dto


# ----------------------------

# Adding ListViews:
@property
def analog_signals(self):
  if not hasattr(self, '_analog_signals'):
    self._analog_signals = ListView(
        self.dto_analog_signals,
        AnalogSignal.newByDTOAnalogSignal,
        AnalogSignal.getDTOAnalogSignal)
  return self._analog_signals

Segment.analog_signals = analog_signals
RecordingChannel.analog_signals = analog_signals
