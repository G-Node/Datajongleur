import numpy as np

import datetime as dt
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
import uuid
import json
from datajongleur import Base, DBSession
from datajongleur.utils.sa import NumpyType, UUID, UUIDMixin
PREFIX = "beanbag_"
#from datajongleur.addendum.models import Addendum, AddendumBadgeMap
from datajongleur.utils.miscellaneous import kwargs2info_dict
from datajongleur.utils.miscellaneous import NumericWithUnits
from datajongleur.utils.sa import addInfoQuantityDBAccess
import datajongleur.beanbags.nwu as nwu

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
    _dto_type = sa.Column('dto_type', sa.String, nullable=False)
    __mapper_args__ = {'polymorphic_on': _dto_type}

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
    
    @classmethod
    def newByUUID(cls, uuid):
        if not hasattr(cls, "session"):
            cls.session = DBSession()
        dto = cls.session.query(cls).filter(
            getattr(cls, 'uuid') == uuid).first()
        return dto

    @classmethod
    def load(cls, uuid):
        return cls.newByUUID(uuid)

    def save(self):
        if not hasattr(self, "session"):
            self.__class__.session = DBSession()
        uuid = self.uuid
        self.session.add (self)
        self.session.commit ()

##########
# Beanbags
##########

class Quantity(NumericWithUnits, Identity):
    __tablename__ = PREFIX + 'quantities'
    __mapper_args__ = {'polymorphic_identity': 'Quantity'}
    uuid = sa.Column(
        sa.ForeignKey(PREFIX + 'identities.uuid'),
        primary_key=True)
    _amount = sa.Column('amount', NumpyType)
    _units = sa.Column('units', sa.String)


class InfoQuantity(nwu.InfoQuantity, Identity):
    __tablename__ = PREFIX + 'info_quantities'
    __mapper_args__ = {'polymorphic_identity': 'InfoQuantity'}
    uuid = sa.Column(
        sa.ForeignKey(PREFIX + 'identities.uuid'),
        primary_key=True)
    _amount = sa.Column('amount', NumpyType)
    _units = sa.Column('units', sa.String)
    info = sa.Column('info', sa.PickleType)


class Point_1D(Identity):
    __tablename__ = PREFIX + 'points_1d'
    __mapper_args__ = {'polymorphic_identity': 'IDPoint'}
    uuid = sa.Column(
        sa.ForeignKey(PREFIX + 'identities.uuid'),
        primary_key=True)
    x = sa.Column('x', sa.Numeric)
    units = sa.Column('units', sa.String)


class Point_2D(Identity):
    __tablename__ = PREFIX + 'points_2d'
    __mapper_args__ = {'polymorphic_identity': 'IIDPoint'}
    uuid = sa.Column(
        sa.ForeignKey(PREFIX + 'identities.uuid'),
        primary_key=True)
    x = sa.Column('x', sa.Numeric)
    y = sa.Column('y', sa.Numeric)
    units = sa.Column('units', sa.String)


class Poind_3D(Identity):
    __tablename__ = PREFIX + 'points_3d'
    __mapper_args__ = {'polymorphic_identity': 'IIIDPoint'}
    uuid = sa.Column(
        sa.ForeignKey(PREFIX + 'identities.uuid'),
        primary_key=True)
    x = sa.Column('x', sa.Numeric)
    y = sa.Column('y', sa.Numeric)
    z = sa.Column('z', sa.Numeric)
    units = sa.Column('units', sa.String)


class TimePoint(nwu.TimePoint, Identity):
    __tablename__ =  PREFIX + 'time_points'
    __mapper_args__ = {'polymorphic_identity': 'TimePoint'}
    uuid = sa.Column(
        sa.ForeignKey(PREFIX + 'identities.uuid'),
        primary_key=True)
    _amount = sa.Column('amount', sa.Float)
    _units = sa.Column('units', sa.String)

    @orm.reconstructor
    def init_on_load(self):
        NumericWithUnits.__init__(self, self._amount, self._units)


class Period(nwu.Period, Identity):
    __tablename__ = PREFIX + 'periods'
    __mapper_args__ = {'polymorphic_identity': 'Period'}
    uuid = sa.Column(
        sa.ForeignKey(PREFIX + 'identities.uuid'),
        primary_key=True)
    _start = sa.Column('start', sa.Float)
    _stop = sa.Column('stop', sa.Float)
    _units = sa.Column('units', sa.String)

    @orm.reconstructor
    def init_on_load(self):
        NumericWithUnits.__init__(self, [self._start, self._stop], self._units)


class SampledSignal(nwu.SampledSignal, Identity):
    __tablename__ = PREFIX + 'regularly_sampled_signal'
    __mapper_args__ = {'polymorphic_identity': 'SampledSignal'}
    uuid = sa.Column(
        sa.ForeignKey(PREFIX + 'identities.uuid'),
        primary_key=True)
    _amount = sa.Column('amount', NumpyType)
    _units = sa.Column('units', sa.String)
    _signal_base_amount = sa.Column('signal_base_amount', NumpyType)
    _signal_base_units = sa.Column('signal_base_units', sa.String)

    def __init__(self, *args, **kwargs):
        nwu.SampledSignal.__init__(self, *args, **kwargs)
        self._signal_base_amount = self.signal_base._amount
        self._signal_base_units = self.signal_base._units

    @orm.reconstructor
    def init_on_load(self):
        NumericWithUnits.__init__(self, self._amount, self._units)
        self.signal_base = NumericWithUnits(
            self._signal_base_amount, self._signal_base_units)


class RegularlySampledSignal(nwu.RegularlySampledSignal, Identity):
    __tablename__ = PREFIX + 'regularly_sampled_time_series'
    __mapper_args__ = {'polymorphic_identity': 'RegularlySampledTimeSeries'}
    uuid = sa.Column(
        sa.ForeignKey(PREFIX + 'identities.uuid'),
        primary_key=True)
    amount = sa.Column('amount', NumpyType)
    units = sa.Column('units', sa.String)
    start = sa.Column('start', sa.Float)
    stop = sa.Column('stop', sa.Float)
    time_units = sa.Column('time_units', sa.String)

    def checksum_json(self):
        return checksum_json(self)
  

def initialize_sql(engine):
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)



if __name__ == '__main__':
    pass
