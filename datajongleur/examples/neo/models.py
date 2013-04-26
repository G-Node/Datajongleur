import sqlalchemy as sa
import sqlalchemy.orm as orm

from datajongleur import Base, DBSession
from datajongleur.ext.neuro.models import *
from datajongleur.ext.neuro.models import PREFIX as NEURO_PREFIX
from datajongleur.beanbags.models import *
from datajongleur.beanbags.models import PREFIX as BB_PREFIX
from datajongleur.utils.sa import NumpyType

PREFIX = 'neo_'
recording_channel_group_recording_channel_maps = sa.Table(
    PREFIX + 'recording_channel_group_recording_channel_maps',
    Base.metadata,
    sa.Column (
      'recording_channel_group_uuid',
      sa.ForeignKey (PREFIX + 'recording_channel_groups.uuid'),
      primary_key=True),
    sa.Column (
      'recording_channel_uuid',
      sa.ForeignKey (PREFIX + 'recording_channels.uuid'),
      primary_key=True),
    )

class Block(DTOIdentity):
  __tablename__ = PREFIX + 'blocks'
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  rec_datetime =  sa.Column('rec_datetime', sa.DateTime)
  file_datetime =  sa.Column('file_datetime', sa.DateTime)
  index = sa.Column('index', sa.Integer)
  __mapper_args__ = {'polymorphic_identity': 'Block',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }

class Segment(DTOIdentity):
  __tablename__ = PREFIX + 'segments'
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  block_uuid =  sa.Column(
      'block_uuid',
      sa.ForeignKey(PREFIX + 'blocks.uuid'),
      )
  rec_datetime =  sa.Column('rec_datetime', sa.DateTime)
  file_datetime =  sa.Column('file_datetime', sa.DateTime)
  index = sa.Column('index', sa.Integer)
  __mapper_args__ = {'polymorphic_identity': 'Segment',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  
  # Properties:
  block = orm.relationship(
      "Block",
      single_parent=True,
      primaryjoin=(block_uuid==Block.uuid),
      foreign_keys=[block_uuid, uuid], # PR: because of inheritance
      uselist=False,
      backref='segments'
      )

class RecordingChannelGroup(DTOIdentity):
  __tablename__ = PREFIX + 'recording_channel_groups'
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  block_uuid =  sa.Column(
      'block_uuid',
      sa.ForeignKey(PREFIX + 'blocks.uuid'),
      )
  channel_names = sa.Column(NumpyType)
  channel_indexes = sa.Column(NumpyType)
  __mapper_args__ = {'polymorphic_identity': 'RecordingChannelGroup',
      'inherit_condition': (uuid==DTOIdentity.uuid)}
  
  block = orm.relationship(
      "Block",
      primaryjoin=(block_uuid==Block.uuid),
      foreign_keys=[block_uuid, uuid], # PR: because of inheritance
      single_parent=True,
      uselist=False,
      backref='recording_channel_groups'
      )


class RecordingChannel(DTOIdentity):
  __tablename__ = PREFIX + 'recording_channels'
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  index = sa.Column('index', sa.Integer)
  # Linking DTOIIDPoint
  iid_point_uuid = sa.Column(
      'iid_point_uuid',
      sa.ForeignKey(BB_PREFIX + 'iid_points.uuid'),
      )
  __mapper_args__ = {
      'polymorphic_identity': 'RecordingChannel',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  # Properties:
  coordinate = orm.relationship(
      "DTOIIDPoint",
      primaryjoin=(iid_point_uuid==DTOIIDPoint.uuid),
      foreign_keys=[iid_point_uuid, uuid] # PR: because of inheritance
      )

  recording_channel_groups = orm.relationship(
      "RecordingChannelGroup",
      secondary=recording_channel_group_recording_channel_maps,
      backref='recording_channels'
      )


class DTOAnalogSignal(DTOIdentity):
  __tablename__ = PREFIX + 'analog_signals'
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  recording_channel_uuid = sa.Column(
      'recording_channel_uuid',
      sa.ForeignKey(PREFIX + 'recording_channels.uuid'),
      )
  segment_uuid = sa.Column('segment_uuid',
      sa.ForeignKey( PREFIX + 'segments.uuid'),
      )
  __mapper_args__ = {'polymorphic_identity': 'AnalogSignal',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  # neuro.beanbags:
  regularly_sampled_time_series_uuid = sa.Column(
        'regularly_sampled_time_series_uuid',
        sa.ForeignKey(NEURO_PREFIX + 'regularly_sampled_time_series.uuid'))
  # Properties:
  recording_channel = orm.relationship(
      "RecordingChannel",
      primaryjoin=(recording_channel_uuid==RecordingChannel.uuid),
      foreign_keys=[recording_channel_uuid, uuid], # PR: because of inheritance
      backref='dto_analog_signals'
      )
  segment = orm.relationship(
      "Segment",
      primaryjoin=(segment_uuid==Segment.uuid),
      foreign_keys=[segment_uuid, uuid], # PR: because of inheritance
      backref='dto_analog_signals'
      )
  dto_regularly_sampled_time_series = orm.relationship(
      "DTORegularlySampledTimeSeries",
      primaryjoin=(regularly_sampled_time_series_uuid==DTORegularlySampledTimeSeries.uuid),
      foreign_keys=[regularly_sampled_time_series_uuid, uuid], # PR: because of inheritance
      backref='dto_analog_signal'
      )


class DTOIrregularlySampledSignal(DTOIdentity):
  __tablename__ = PREFIX + 'irregularly_sampled_signals_dtos'
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  recording_channel_uuid = sa.Column(
      'recording_channel_uuid',
      sa.ForeignKey(PREFIX + 'recording_channels.uuid'),
      )
  segment_uuid = sa.Column('segment_uuid',
      sa.ForeignKey( PREFIX + 'segments.uuid'),
      )
  # neuro.beanbags:
  regularly_sampled_time_series_uuid = sa.Column(
        'sampled_time_series_uuid',
        sa.ForeignKey(NEURO_PREFIX + 'sampled_time_series.uuid'))
  __mapper_args__ = {'polymorphic_identity': 'IrregularlySampledSignal',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  # Properties:
  recording_channels = orm.relationship(
      "RecordingChannel",
      primaryjoin=(recording_channel_uuid==RecordingChannel.uuid),
      foreign_keys=[recording_channel_uuid, uuid], # PR: because of inheritance
      backref='irregularly_sampled_signals'
      )
  segments = orm.relationship(
      "Segment",
      primaryjoin=(segment_uuid==Segment.uuid),
      foreign_keys=[segment_uuid, uuid], # PR: because of inheritance
      backref='irregularly_sampled_signals'
      )


class DTOEvent(DTOIdentity):
  __tablename__ = PREFIX + 'events'
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  segment_uuid = sa.Column('segment_uuid',
      sa.ForeignKey( PREFIX + 'segments.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  __mapper_args__ = {'polymorphic_identity': 'Event',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  # Datajongleur link
  dto_id_point_uuid = sa.Column(
      'dto_iid_point_uuid',
      sa.ForeignKey(BB_PREFIX + 'iid_points.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  # Properties:
  segments = orm.relationship(
      "Segment",
      primaryjoin=(segment_uuid==Segment.uuid),
      backref='events'
      )
  timepoint = orm.relationship(
      "DTOIDPoint",
      primaryjoin=(dto_id_point_uuid==DTOIDPoint.uuid)
      )

class DTOEventArray(DTOIdentity):
  __tablename__ = PREFIX + 'event_arrays'
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  segment_uuid = sa.Column('segment_uuid',
      sa.ForeignKey( PREFIX + 'segments.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  __mapper_args__ = {'polymorphic_identity': 'EventArray',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  # Datajongleur link
  dto_quantity_uuid = sa.Column(
      'dto_quantity_uuid',
      sa.ForeignKey(BB_PREFIX + 'quantities.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  # Properties:
  segments = orm.relationship(
      "Segment",
      primaryjoin=(segment_uuid==Segment.uuid),
      backref='event_arrays'
      )
  quantity = orm.relationship(
      "DTOQuantity",
      primaryjoin=(dto_quantity_uuid==DTOQuantity.uuid)
      )


class DTOEpoch(DTOIdentity):
  __tablename__ = PREFIX + 'epochs'
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  segment_uuid = sa.Column('segment_uuid',
      sa.ForeignKey( PREFIX + 'segments.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  __mapper_args__ = {'polymorphic_identity': 'Epoch',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  # Datajongleur link
  dto_period_uuid = sa.Column(
      'dto_iid_point_uuid',
      sa.ForeignKey(NEURO_PREFIX + 'periods.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  # Properties:
  segments = orm.relationship(
      "Segment",
      primaryjoin=(segment_uuid==Segment.uuid),
      backref='epochs'
      )
  period = orm.relationship(
      "DTOPeriod",
      primaryjoin=(dto_period_uuid==DTOPeriod.uuid)
      )


class Unit(DTOIdentity):
  __tablename__ = PREFIX + 'units'
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  recording_channel_group_uuid =  sa.Column(
      'recording_channel_group_uuid',
      sa.ForeignKey(PREFIX + 'recording_channel_groups.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      nullable=True)
  __mapper_args__ = {
      'polymorphic_identity': 'Unit',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  # Properties:
  recording_channel_groups = orm.relationship(
      "RecordingChannelGroup",
      primaryjoin=(
        recording_channel_group_uuid==RecordingChannelGroup.uuid),
      backref='units'
      )


class DTOSpikeTrain(DTOIdentity):
  __tablename__ = PREFIX + 'spike_trains'
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  unit_uuid =  sa.Column(
      'unit_uuid',
      sa.ForeignKey(PREFIX + 'units.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      nullable=True)
  __mapper_args__ = {
      'polymorphic_identity': 'SpikeTrain',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  # Datajongleur References
  dto_spike_times_uuid = sa.Column(
      'dto_spike_times_uuid',
      sa.ForeignKey(NEURO_PREFIX + 'spike_times.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      ) # -> ``SpikeTrain.times``
  waveforms_dto_quantities_uuid = sa.Column(
      'waveforms_dto_quantity_uuid',
      sa.ForeignKey(BB_PREFIX + 'quantities.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  leftsweep_dto_quantities_uuid = sa.Column(
      'leftsweep_dto_quantity_uuid',
      sa.ForeignKey(BB_PREFIX + 'quantities.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  sampling_rate_dto_id_points_uuid = sa.Column(
      'sampling_rate_dto_id_point_uuid',
      sa.ForeignKey(BB_PREFIX + 'id_points.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )

  # Properties:
  spike_times = orm.relationship(
      "DTOSpikeTimes",
      primaryjoin=(dto_spike_times_uuid==DTOSpikeTimes.uuid)
      )
  waveforms_dto_quantity = orm.relationship(
      "DTOQuantity",
      primaryjoin=(waveforms_dto_quantities_uuid==DTOQuantity.uuid)
      )
  leftsweep_dto_quantity = orm.relationship(
      "DTOQuantity",
      primaryjoin=(leftsweep_dto_quantities_uuid==DTOQuantity.uuid)
      )
  sampling_rate_dto_id_point = orm.relationship(
      "DTOQuantity",
      primaryjoin=(sampling_rate_dto_id_points_uuid==DTOIDPoint.uuid)
      )
  unit = orm.relationship(
      "RecordingChannelGroup",
      primaryjoin=(
        unit_uuid==Unit.uuid),
      backref='spike_trains',
      uselist=False
      )

  
class DTOSpike(DTOIdentity):
  __tablename__ = PREFIX + 'spikes'
  uuid = sa.Column(
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      primary_key=True)
  unit_uuid =  sa.Column(
      'unit_uuid',
      sa.ForeignKey(PREFIX + 'units.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      nullable=True)
  __mapper_args__ = {
      'polymorphic_identity': 'SpikeTrain',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  # Datajongleur References
  time_dto_id_point_uuid = sa.Column(
      'time_dto_id_point_uuid',
      sa.ForeignKey(BB_PREFIX + 'id_points.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      ) # -> ``SpikeTrain.times``
  waveform_dto_sampled_time_series_uuid = sa.Column(
      'waveform_dto_sampled_time_series_uuid',
      sa.ForeignKey(NEURO_PREFIX + 'sampled_time_series.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  leftsweep_dto_quantities_uuid = sa.Column(
      'leftsweep_dto_quantity_uuid',
      sa.ForeignKey(BB_PREFIX + 'quantities.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )

  # Properties:
  unit = orm.relationship(
      "RecordingChannelGroup",
      primaryjoin=(
        unit_uuid==Unit.uuid),
      backref='spikes',
      uselist=False
      )
  time_dto_id_point = orm.relationship(
      "DTOSpikeTimes",
      primaryjoin=(time_dto_id_point_uuid==DTOIDPoint.uuid)
      )
  waveform_dto_sampled_time_series = orm.relationship(
      "DTOQuantity",
      primaryjoin=(
        waveform_dto_sampled_time_series_uuid==DTOSampledTimeSeries.uuid)
      )
  leftsweep_dto_quantity = orm.relationship(
      "DTOQuantity",
      primaryjoin=(leftsweep_dto_quantities_uuid==DTOQuantity.uuid)
      )
