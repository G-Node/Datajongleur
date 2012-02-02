import datetime as dt
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
import uuid
from datajongleur import Base, DBSession
from datajongleur.utils.sa import NumpyType, UUID, UUIDMixin
PREFIX = "beanbag_"
from datajongleur.addendum.models import Addendum, AddendumBadgeMap

##########
# Identity
##########

class DTOIdentity(UUIDMixin, Base):
  __tablename__ = PREFIX + 'identities'
  modification_time = sa.Column(
      'modification_time', 
      sa.DateTime,
      default=dt.datetime.now())
  dto_type = sa.Column(sa.String, nullable=False)
  __mapper_args__ = {'polymorphic_on': dto_type}

  # Property ``addendum_object`` is defined as backref within ``Addendum``
  def add_badge(self, badge_dict={}, **kwargs):
    if self.addendum_object is None:
      self.addendum_object = Addendum()
    badge_dict.update(kwargs)
    self.addendum_object.badges = badge_dict

  _name = association_proxy('addendum_object', 'name',
      creator=lambda name: Addendum(
        name=name, description='', flag=False))
  _description = association_proxy('addendum_object', 'description',
      creator=lambda description: Addendum(
        name='', description=description, flag=False))
  _flag = association_proxy('addendum_object', 'flag',
      creator=lambda flag: Addendum(
        name='', description='', flag=flag))

  @property
  def badges(self):
    try:
      return self.addendum_object.badges
    except AttributeError:
      "In case that there is no ``Addendum`` specified, yet."
      return None

  @badges.setter
  def badges(self, value):
    self.add_badge(value)

  @property
  def name(self):
    try:
      return self._name
    except AttributeError:
      "In case that there is no ``Addendum`` specified, yet."
      return ""

  @name.setter
  def name(self, value):
    self._name = value

  @property
  def description(self):
    try:
      return self._description
    except AttributeError:
      "In case that there is no ``Addendum`` specified, yet."
      return ""

  @description.setter
  def description(self, value):
    self._description = value

  @property
  def flag(self):
    try:
      return self._flag
    except AttributeError:
      "In case that there is no ``Addendum`` specified, yet."
      return ""

  @flag.setter
  def flag(self, value):
    self._flag = value

##########
# Beanbags
##########

class DTOQuantity(DTOIdentity):
  __tablename__ = PREFIX + 'quantities'
  __mapper_args__ = {'polymorphic_identity': 'Quantity'}
  uuid = sa.Column(
      sa.ForeignKey(PREFIX + 'identities.uuid'),
      primary_key=True)
  amount = sa.Column('amount', NumpyType)
  units = sa.Column('units', sa.String)

class DTOIDPoint(DTOIdentity):
  __tablename__ = PREFIX + 'id_points'
  __mapper_args__ = {'polymorphic_identity': 'IDPoint'}
  uuid = sa.Column(
      sa.ForeignKey(PREFIX + 'identities.uuid'),
      primary_key=True)
  x = sa.Column('x', sa.Numeric)
  units = sa.Column('units', sa.String)

class DTOIIDPoint(DTOIdentity):
  __tablename__ = PREFIX + 'iid_points'
  __mapper_args__ = {'polymorphic_identity': 'IIDPoint'}
  uuid = sa.Column(
      sa.ForeignKey(PREFIX + 'identities.uuid'),
      primary_key=True)
  x = sa.Column('x', sa.Numeric)
  y = sa.Column('y', sa.Numeric)
  units = sa.Column('units', sa.String)

class DTOIIIDPoint(DTOIdentity):
  __tablename__ = PREFIX + 'iiid_points'
  __mapper_args__ = {'polymorphic_identity': 'IIIDPoint'}
  uuid = sa.Column(
      sa.ForeignKey(PREFIX + 'identities.uuid'),
      primary_key=True)
  x = sa.Column('x', sa.Numeric)
  y = sa.Column('y', sa.Numeric)
  z = sa.Column('z', sa.Numeric)
  units = sa.Column('units', sa.String)

def initialize_sql(engine):
  Base.metadata.bind = engine
  Base.metadata.create_all(engine)
