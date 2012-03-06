import numpy as np

import datetime as dt
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
import uuid
import json
from datajongleur import Base, CurrentNumeric
from datajongleur.utils.sa import NumpyType, UUID, UUIDMixin
PREFIX = "beanbag_"
from datajongleur.addendum.models import Addendum, AddendumBadgeMap
from datajongleur.utils.miscellaneous import kwargs2info_dict
from datajongleur.utils.miscellaneous import Numeric

def catchAttributeError(func):
  def dec(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except AttributeError:
      "In case that there is no ``Addendum`` specified, yet."
      return None
  return dec

##########
# Identity
##########

class DTOIdentity(UUIDMixin, Base):
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

class DTOQuantity(DTOIdentity):
  __tablename__ = PREFIX + 'quantities'
  __mapper_args__ = {'polymorphic_identity': 'Quantity'}
  uuid = sa.Column(
      sa.ForeignKey(PREFIX + 'identities.uuid'),
      primary_key=True)
  amount = sa.Column('amount', NumpyType)
  units = sa.Column('units', sa.String)


class InfoQuantity(DTOIdentity, Numeric):
  __tablename__ = PREFIX + 'info_quantities'
  __mapper_args__ = {'polymorphic_identity': 'InfoQuantity'}
  uuid = sa.Column(
      sa.ForeignKey(PREFIX + 'identities.uuid'),
      primary_key=True)
  _amount = sa.Column('amount', NumpyType)
  _units = sa.Column('units', sa.String)
  info = sa.Column('info', sa.PickleType)

  def __init__(self, amount, units='', **kwargs):
    if type(amount)==type(self):
      self._amount = amount.amount
      self._units = amount.units
      kwargs.update(amount.info)
    elif type(amount)==CurrentNumeric: # Quantity - if installed
      signal = amount
      self._amount = signal.view(np.ndarray)
      if hasattr(signal, 'dimensionality'):
        self._units = signal.dimensionality.string
    else:
      self._amount = np.array(amount)
      self._units = units
    self.set_signal(CurrentNumeric(self.amount, self.units))
    self.info = kwargs2info_dict(kwargs)

  @property
  def amount(self):
    return self._amount

  @property
  def units(self):
    return self._units

  def __str_main__ (self):
    """ Representation of the inherited Quantity-part"""
    return "%r\n" % self.signal
    
  def __str_info__ (self):
    if len(self.info.keys()) == 0:
      return ""
    str_info = "Info-Attributes:\n"
    for info_attribute in self.info.iteritems():
      str_info += " %s: %r\n" %(info_attribute[0], info_attribute[1])
    return str_info
  
  def __str__(self):
    head = ">>> %s <<<\n" %(self.__class__.__name__)
    str_string = "%s\n%s" % (self.__str_main__(), self.__str_info__())
    return head + str_string[:-1]

  def __repr__(self):
    return "%s(%s, %r, info)" %(
        self.__class__.__name__,
        self.amount,
        self.units)

  @property
  def hash(self):
    return sha1(self.__str__()).hexdigest()
  
  def __hash__(self):
    return self.hash


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
