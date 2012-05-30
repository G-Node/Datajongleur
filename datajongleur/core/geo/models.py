import sqlalchemy as sa
import sqlalchemy.orm as orm
import numpy as np
import json
import uuid
from datajongleur import Base
from datajongleur.utils.sa import NumpyType, UUID
from datajongleur.beanbags.models import Identity
from datajongleur.beanbags.models import PREFIX as BB_PREFIX

class IDPoint(Identity):
  __tablename__ = PREFIX + 'id_points'
  __mapper_args__ = {'polymorphic_identity': 'IDPoint'}
  uuid = sa.Column(
      sa.ForeignKey(PREFIX + 'identities.uuid'),
      primary_key=True)
  x = sa.Column('x', sa.Numeric)
  units = sa.Column('units', sa.String)


class IIDPoint(Identity):
  __tablename__ = PREFIX + 'iid_points'
  __mapper_args__ = {'polymorphic_identity': 'IIDPoint'}
  uuid = sa.Column(
      sa.ForeignKey(PREFIX + 'identities.uuid'),
      primary_key=True)
  x = sa.Column('x', sa.Numeric)
  y = sa.Column('y', sa.Numeric)
  units = sa.Column('units', sa.String)


class IIIDPoint(Identity):
  __tablename__ = PREFIX + 'iiid_points'
  __mapper_args__ = {'polymorphic_identity': 'IIIDPoint'}
  uuid = sa.Column(
      sa.ForeignKey(PREFIX + 'identities.uuid'),
      primary_key=True)
  x = sa.Column('x', sa.Numeric)
  y = sa.Column('y', sa.Numeric)
  z = sa.Column('z', sa.Numeric)
  units = sa.Column('units', sa.String)
