from datajongleur.neuro.models import *

PREFIX = 'neo_'

class DTOBlock(object):
  __tablename__ = PREFIX + 'blocks'
  
  key =  sa.Column('key', sa.Integer, primary_key=True)
  uuid = sa.Column('uuid', GUID, unique=True,
      default=uuid.uuid4)
  rec_datetime =  sa.Column('rec_datetime', sa.DateTime)
  file_datetime =  sa.Column('file_datetime', sa.DateTime)
  index = sa.Column('index', sa.Integer)


class DTOSegment(object):
  __tablename__ = PREFIX + 'segments'

  key =  sa.Column('key', sa.Integer, primary_key=True)
  uuid = sa.Column('uuid', GUID, unique=True,
      default=uuid.uuid4)
  block_key =  sa.Column(
      'block_key',
      sa.Integer,
      sa.ForeignKey(PREFIX + 'blocks.key'),
      #nullable=False) #PR: check!
      )
  rec_datetime =  sa.Column('rec_datetime', sa.DateTime)
  file_datetime =  sa.Column('file_datetime', sa.DateTime)
  index = sa.Column('index', sa.Integer)


class DTORecordingChannelGroup(object):
  __tablename__ = PREFIX + 'recording_channel_groups'
  recording_channel_group_key = sa.Column(
      'recording_channel_group_key', sa.Integer, primary_key=True),


class DTORecordingChannel(object):
  __tablename__ = PREFIX + 'recording_channels'
  recording_channel_key =  sa.Column(
      'recording_channel_key', sa.Integer, primary_key=True)
  recording_channel_group_key =  sa.Column(
      'recording_channel_group_key',
      sa.Integer,
      sa.ForeignKey(
        PREFIX + 'recording_channel_groups.recording_channel_group_key'),
      nullable=False)
  index = sa.Column('index', sa.Integer)


class DTOAnalogSignal(object):
  __tablename__ = PREFIX + 'analog_signal_dtos'
  __table_args__ = (

      sa.ForeignKeyConstraint(
        ['recording_channel_key'],
        [schemaname+"."+PREFIX+'recording_channels.recording_channel_key']),
      sa.ForeignKeyConstraint(
        ['segment_key'],
        [schemaname + "." + PREFIX + 'segments.segment_key']),
      sa.ForeignKeyConstraint(
        ['regularly_sampled_time_series_key'],
        [schemaname + "." + djnPREFIX +\
          'regularly_sampled_time_series.regularly_sampled_time_series_key']),
      {})
  analog_signal_key =  sa.Column(
      'analog_signal_key', sa.Integer, primary_key=True),
  segment_key = sa.Column('segment_key', sa.Integer, nullable=False),
  recording_channel_key = sa.Column(
      'recording_channel_key', sa.Integer), #PR: nullable=False),
  # Datajongleur link
  regularly_sampled_time_series_key = sa.Column(
      'regularly_sampled_time_series_key', sa.BigInteger,
      nullable=False),

"""
@addAddendumAccess("_dto_analog_signal")
class AnalogSignal(djcls.RegularlySampledTimeSeries):
  def __init__(self, *args, **kwargs):
    # real initialization takes place at
    # ``RegularlySampledTimeSeries.__newByDTO__(...)``
    # => initial usage equivalent to ``RegularlySampledTimeSeries``
    #
    # initialize default-attributes for structural inforamtion of
    # AnalogSignalsa
    self._dto_analog_signal = AnalogSignalDTO()
    self._addendum = self._dto_analog_signal._addendum
 
  def get_my_special_signal(self):
    print "super signal"
  
  def getFavorite(self):
    return self._dto_analog_signal.favorite

  def setFavorite(self, value):
    self._dto_analog_signal.favorite = value

  def getDescription(self):
    return self._dto_analog_signal.description

  def setDescription(self, value):
    self._dto_analog_signal.value = value

  def getRegularlySampledTimeSeries(self):
    return djcls.RegularlySampledTimeSeries.newByDTO(self._dto_rsts)

  favorite = property(getFavorite, setFavorite)
  description = property(getDescription, setDescription)
"""

class DTOEvent(object):
      sa.Column('event_key', sa.Integer, primary_key=True),
      sa.Column('segment_key', sa.Integer, nullable=False),
      # required attributes (neo 0.2)
      # recommended attributes (neo 0.2)
      # g-node specific attributes
      # system attributs
      sa.Column('name', sa.String, unique=True),
      sa.Column('description', sa.String),
      sa.Column('favorite', sa.Boolean, nullable=False, default=False),
      # Datajongleur link
      sa.Column('time_point_key', sa.BigInteger,
        nullable=False),
      # Constraints
      sa.ForeignKeyConstraint(
        ['time_point_key'],
        [schemaname + "." + djnPREFIX +\
          'time_points.time_point_key']),
      sa.ForeignKeyConstraint(
        ['segment_key'],
        [schemaname + "." + PREFIX + 'segments.segment_key']),
