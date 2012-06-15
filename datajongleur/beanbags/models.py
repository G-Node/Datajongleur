import numpy as np
import datetime as dt
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from datajongleur import Base, DBSession
from datajongleur.utils.sa import NumpyType, UUID, UUIDMixin
PREFIX = "beanbag_"
from datajongleur.addendum.models import Addendum, AddendumBadgeMap
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

identity_tag_maps = sa.Table(
    PREFIX + 'identity_tag_maps',
    Base.metadata,
    sa.Column('identity_uuid', sa.ForeignKey(PREFIX + 'identities.uuid'), primary_key=True),
    sa.Column('tag_uuid', sa.ForeignKey(PREFIX + 'tags.uuid'), primary_key=True))


def find_or_create_tag(kw):
    tag = Tag.query.filter_by(name=kw).first()
    if not(tag):
        tag = Tag(name=kw)
        # if aufoflush=False used in the session, then uncomment below
        if not hasattr(Tag, "session"):
            Tag.session = DBSession()
        Tag.session.add(tag)
        Tag.session.flush()
    return tag


class Tag(UUIDMixin, Base):
    __tablename__ = PREFIX + 'tags'
    name = sa.Column(sa.String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

@addInfoQuantityDBAccess
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


    # tags & proxy the 'keyword' attribute from the 'kw' relationship
    tag_objects = orm.relationship('Tag',
        secondary=identity_tag_maps,
        backref='tagged')
    tags = association_proxy('tag_objects', 'name',
        creator=find_or_create_tag)

    # Addendum proxies
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

class Quantity(nwu.NumericWithUnits, Identity):
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
        nwu.NumericWithUnits.__init__(self, self._amount, self._units)


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
        nwu.NumericWithUnits.__init__(self, [self._start, self._stop], self._units)


class SampledSignal(nwu.SampledSignal, Identity):
    __tablename__ = PREFIX + 'sampled_signal'
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
        nwu.NumericWithUnits.__init__(self, self._amount, self._units)
        self.signal_base = nwu.NumericWithUnits(
            self._signal_base_amount, self._signal_base_units)


class RegularlySampledSignal(nwu.RegularlySampledSignal, Identity):
    """
    Usage: >>> rss = RegularlySampledSignal([1,2,3], 'mV', [0, 5], 'ms')
    """
    __tablename__ = PREFIX + 'regularly_sampled_signal'
    __mapper_args__ = {'polymorphic_identity': 'RegularlySampledSignal'}
    uuid = sa.Column(
        sa.ForeignKey(PREFIX + 'identities.uuid'),
        primary_key=True)
    _amount = sa.Column('amount', NumpyType)
    _units = sa.Column('units', sa.String)
    _sample_start = sa.Column('start', sa.Float)
    _sample_stop = sa.Column('stop', sa.Float)
    _sample_units = sa.Column('time_units', sa.String)

    def __init__(self, *args, **kwargs):
        nwu.RegularlySampledSignal.__init__(self, *args, **kwargs)
        self._sample_start         = self.start
        self._sample_stop          = self.stop
        self._sample_units    = self.period.units

    @orm.reconstructor
    def init_on_load(self):
        """
        nwu.NumericWithUnits.__init__(self, self._amount, self._units)
        self.period = Period(
                [self._sample_start, self._sample_stop],
                self._sample_units)
        """
        nwu.RegularlySampledSignal.__init__(
                self,
                self._amount,
                self._units,
                [self._sample_start, self._sample_stop],
                self._sample_units)

    @property
    def info(self):
        return {'period': self.period}


def initialize_sql(engine):
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    pass