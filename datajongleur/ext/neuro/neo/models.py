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

class DTOBlock(DTOIdentity):
  __tablename__ = PREFIX + 'blocks'
  __mapper_args__ = {'polymorphic_identity': 'Block',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  rec_datetime =  sa.Column('rec_datetime', sa.DateTime)
  file_datetime =  sa.Column('file_datetime', sa.DateTime)
  index = sa.Column('index', sa.Integer)

class DTOSegment(DTOIdentity):
  __tablename__ = PREFIX + 'segments'
  __mapper_args__ = {'polymorphic_identity': 'Segment',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  block_uuid =  sa.Column(
      'block_uuid',
      sa.ForeignKey(PREFIX + 'blocks.uuid'),
      )
  rec_datetime =  sa.Column('rec_datetime', sa.DateTime)
  file_datetime =  sa.Column('file_datetime', sa.DateTime)
  index = sa.Column('index', sa.Integer)
  
  # Properties:
  block_object = orm.relationship(
      "DTOBlock",
      single_parent=True,
      primaryjoin=(block_uuid==DTOBlock.uuid),
      foreign_keys=[block_uuid, uuid], # PR: because of inheritance
      uselist=False,
      backref='segment_objects'
      )

class DTORecordingChannelGroup(DTOIdentity):
  __tablename__ = PREFIX + 'recording_channel_groups'
  __mapper_args__ = {'polymorphic_identity': 'RecordingChannelGroup',
      'inherit_condition': (uuid==DTOIdentity.uuid)}
  block_uuid =  sa.Column(
      'block_uuid',
      sa.ForeignKey(PREFIX + 'blocks.uuid'),
      )
  channel_names = sa.Column(NumpyType)
  channel_indexes = sa.Column(NumpyType)
  
  block_object = orm.relationship(
      "DTOBlock",
      primaryjoin=(block_uuid==DTOBlock.uuid),
      foreign_keys=[block_uuid, uuid], # PR: because of inheritance
      single_parent=True,
      uselist=False,
      backref='recording_channel_group_objects'
      )
class DTORecordingChannel(DTOIdentity):
  __tablename__ = PREFIX + 'recording_channels'
  __mapper_args__ = {
      'polymorphic_identity': 'RecordingChannel',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  index = sa.Column('index', sa.Integer)
  # Linking DTOIIDPoint
  iid_point_uuid = sa.Column(
      'iid_point_uuid',
      sa.ForeignKey(BB_PREFIX + 'iid_points.uuid'),
      )
  # Properties:
  coordinate_object = orm.relationship(
      "DTOIIDPoint",
      primaryjoin=(iid_point_uuid==DTOIIDPoint.uuid),
      foreign_keys=[iid_point_uuid, uuid] # PR: because of inheritance
      )

  recording_channel_group_objects = orm.relationship(
      "DTORecordingChannelGroup",
      secondary=recording_channel_group_recording_channel_maps,
      backref='recording_channel_objects'
      )


class DTOAnalogSignal(DTOIdentity):
  __tablename__ = PREFIX + 'analog_signals'
  __mapper_args__ = {'polymorphic_identity': 'AnalogSignal',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  recording_channel_uuid = sa.Column(
      'recording_channel_uuid',
      sa.ForeignKey(PREFIX + 'recording_channels.uuid'),
      )
  segment_uuid = sa.Column('segment_uuid',
      sa.ForeignKey( PREFIX + 'segments.uuid'),
      )
  # neuro.beanbags:
  regularly_sampled_time_series_uuid = sa.Column(
        'regularly_sampled_time_series_uuid',
        sa.ForeignKey(NEURO_PREFIX + 'regularly_sampled_time_series.uuid'))
  # Properties:
  recording_channel_objects = orm.relationship(
      "DTORecordingChannel",
      primaryjoin=(recording_channel_uuid==DTORecordingChannel.uuid),
      foreign_keys=[recording_channel_uuid, uuid], # PR: because of inheritance
      backref='analog_signal_objects'
      )
  segment_objects = orm.relationship(
      "DTOSegment",
      primaryjoin=(segment_uuid==DTOSegment.uuid),
      foreign_keys=[segment_uuid, uuid], # PR: because of inheritance
      backref='analog_signal_objects'
      )


class DTOIrregularlySampledSignal(DTOIdentity):
  __tablename__ = PREFIX + 'irregularly_sampled_signals_dtos'
  __mapper_args__ = {'polymorphic_identity': 'IrregularlySampledSignal',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
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
  # Properties:
  recording_channel_objects = orm.relationship(
      "DTORecordingChannel",
      primaryjoin=(recording_channel_uuid==DTORecordingChannel.uuid),
      foreign_keys=[recording_channel_uuid, uuid], # PR: because of inheritance
      backref='irregularly_sampled_signal_objects'
      )
  segment_objects = orm.relationship(
      "DTOSegment",
      primaryjoin=(segment_uuid==DTOSegment.uuid),
      foreign_keys=[segment_uuid, uuid], # PR: because of inheritance
      backref='irregularly_sampled_signal_objects'
      )


class DTOEvent(DTOIdentity):
  __tablename__ = PREFIX + 'events'
  __mapper_args__ = {'polymorphic_identity': 'Event',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  segment_uuid = sa.Column('segment_uuid',
      sa.ForeignKey( PREFIX + 'segments.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  # Datajongleur link
  dto_id_point_uuid = sa.Column(
      'dto_iid_point_uuid',
      sa.ForeignKey(BB_PREFIX + 'iid_points.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  # Properties:
  segment_objects = orm.relationship(
      "DTOSegment",
      primaryjoin=(segment_uuid==DTOSegment.uuid),
      backref='event_objects'
      )
  timepoint_object = orm.relationship(
      "DTOIDPoint",
      primaryjoin=(dto_id_point_uuid==DTOIDPoint.uuid)
      )

class DTOEventArray(DTOIdentity):
  __tablename__ = PREFIX + 'event_arrays'
  __mapper_args__ = {'polymorphic_identity': 'EventArray',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  segment_uuid = sa.Column('segment_uuid',
      sa.ForeignKey( PREFIX + 'segments.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  # Datajongleur link
  dto_quantity_uuid = sa.Column(
      'dto_quantity_uuid',
      sa.ForeignKey(BB_PREFIX + 'quantities.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  # Properties:
  segment_objects = orm.relationship(
      "DTOSegment",
      primaryjoin=(segment_uuid==DTOSegment.uuid),
      backref='event_array_objects'
      )
  quantity_object = orm.relationship(
      "DTOQuantity",
      primaryjoin=(dto_quantity_uuid==DTOQuantity.uuid)
      )


class DTOEpoch(DTOIdentity):
  __tablename__ = PREFIX + 'epochs'
  __mapper_args__ = {'polymorphic_identity': 'Epoch',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  segment_uuid = sa.Column('segment_uuid',
      sa.ForeignKey( PREFIX + 'segments.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  # Datajongleur link
  dto_period_uuid = sa.Column(
      'dto_iid_point_uuid',
      sa.ForeignKey(NEURO_PREFIX + 'periods.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      )
  # Properties:
  segment_objects = orm.relationship(
      "DTOSegment",
      primaryjoin=(segment_uuid==DTOSegment.uuid),
      backref='epoch_objects'
      )
  period_object = orm.relationship(
      "DTOPeriod",
      primaryjoin=(dto_period_uuid==DTOPeriod.uuid)
      )


class DTOUnit(DTOIdentity):
  __tablename__ = PREFIX + 'units'
  __mapper_args__ = {
      'polymorphic_identity': 'Unit',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  recording_channel_group_uuid =  sa.Column(
      'recording_channel_group_uuid',
      sa.ForeignKey(PREFIX + 'recording_channel_groups.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      nullable=False)
  # Properties:
  recording_channel_group_objects = orm.relationship(
      "DTORecordingChannelGroup",
      primaryjoin=(
        recording_channel_group_uuid==DTORecordingChannelGroup.uuid),
      backref='unit_objects'
      )


class DTOSpikeTrain(DTOIdentity):
  __tablename__ = PREFIX + 'spike_trains'
  __mapper_args__ = {
      'polymorphic_identity': 'SpikeTrain',
      'inherit_condition': (uuid==DTOIdentity.uuid)
      }
  unit_uuid =  sa.Column(
      'unit_uuid',
      sa.ForeignKey(PREFIX + 'units.uuid'),
      sa.ForeignKey(BB_PREFIX + 'identities.uuid'),
      nullable=False)
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
  spike_times_object = orm.relationship(
      "DTOSpikeTimes",
      primaryjoin=(dto_spike_times_uuid==DTOSpikeTimes.uuid)
      )
  waveforms_dto_quantity_object = orm.relationship(
      "DTOQuantity",
      primaryjoin=(waveforms_dto_quantities_uuid==DTOQuantity.uuid)
      )
  leftsweep_dto_quantity_object = orm.relationship(
      "DTOQuantity",
      primaryjoin=(leftsweep_dto_quantities_uuid==DTOQuantity.uuid)
      )
  sampling_rate_dto_id_point_object = orm.relationship(
      "DTOQuantity",
      primaryjoin=(sampling_rate_dto_id_points_uuid==DTOIDPoint.uuid)
      )
  unit_object = orm.relationship(
      "DTORecordingChannelGroup",
      primaryjoin=(
        unit_uuid==DTOUnit.uuid),
      backref='spike_train_objects',
      uselist=False
      )
"""
"""
