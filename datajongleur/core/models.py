import numpy as np
import datetime as dt
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
import uuid
import json

PREFIX = "beanbag_"

import datajongleur.core.beanbags as core_bb
from datajongleur import Base
from datajongleur.utils.sa import NumpyType, UUID, UUIDMixin
from datajongleur.addendum.models import Addendum, AddendumBadgeMap
from datajongleur.utils.miscellaneous import kwargs2info_dict
from datajongleur.core.beanbags import NumericWithUnits
from datajongleur.utils.sa import addInfoQuantityDBAccess


def catchAttributeError(func):
  def decorator(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except AttributeError:
      "In case that there is no ``Addendum`` specified, yet."
      return None
  return decorator

##########
# Identity
##########

class Identity(UUIDMixin, Base):
  __tablename__ = PREFIX + 'identities'
  mtime = sa.Column(
      'mtime', 
      sa.DateTime,
      default=dt.datetime.now())
  ctime = sa.Column(
      'ctime', 
      sa.DateTime,
      default=dt.datetime.now())
  dto_type = sa.Column(sa.String, nullable=False)
  __mapper_args__ = {'polymorphic_on': dto_type}

  _name = association_proxy('addendum', 'name',
      creator=lambda name: Addendum(
        name=name, description='', flag=False))
  _description = association_proxy('addendum', 'description',
      creator=lambda description: Addendum(
        name='', description=description, flag=False))
  _flag = association_proxy('addendum', 'flag',
      creator=lambda flag: Addendum(
        name='', description='', flag=flag))
  _badges = association_proxy ('addendum', 'badges',
      creator=lambda badges: Addendum(
        name='', description='', flag=False, badges=badges))

  @property
  @catchAttributeError
  def badges(self):
    return self._badges

  @badges.setter
  def badges(self, value):
    self._badges = value

  @property
  @catchAttributeError
  def name(self):
    return self._name

  @name.setter
  def name(self, value):
    self._name = value

  @property
  @catchAttributeError
  def description(self):
    return self._description

  @description.setter
  def description(self, value):
    self._description = value

  @property
  @catchAttributeError
  def flag(self):
    return self._flag

  @flag.setter
  def flag(self, value):
    self._flag = value

##########
# Beanbags
##########

@addInfoQuantityDBAccess
class InfoQuantity(core_bb.InfoQuantity, Identity):
  __tablename__ = PREFIX + 'info_quantities'
  __mapper_args__ = {'polymorphic_identity': 'InfoQuantity'}
  uuid = sa.Column(
      sa.ForeignKey(PREFIX + 'identities.uuid'),
      primary_key=True)
  _amount = sa.Column('amount', NumpyType)
  _units = sa.Column('units', sa.String)
  _info = sa.Column('info', sa.PickleType)


def initialize_sql(engine):
  Base.metadata.bind = engine
  Base.metadata.create_all(engine)
