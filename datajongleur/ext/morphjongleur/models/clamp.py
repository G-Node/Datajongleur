# -*- coding: utf-8 -*-
'''
@author: stransky
'''
import sqlalchemy.orm
from datajongleur import Base
from datajongleur.beanbags.models import Identity
from datajongleur.beanbags.models import PREFIX as BB_PREFIX
from datajongleur.beanbags.models import *
import mrj.model.clamp
import mrj.util.auto_string

PREFIX = 'mrj_'

class VClamp(mrj.model.clamp.VClamp, Identity):
    __tablename__   = PREFIX + 'vclamps'
    vclamp_key      = sqlalchemy.Column(
        sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True)
    experiment_key  = sqlalchemy.Column(
        sqlalchemy.ForeignKey(PREFIX + 'experiments.experiment_key'))
    morphology_key  = sqlalchemy.Column(
        sqlalchemy.ForeignKey(PREFIX + 'morphologies.morphology_key'))
    compartment_key = sqlalchemy.Column('compartment_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(PREFIX + 'compartments.compartment_key'))
    compartment_id  = sqlalchemy.Column('compartment_id', sqlalchemy.Integer)
    position        = sqlalchemy.Column('position', sqlalchemy.Float)


class IClamp(mrj.model.clamp.IClamp, Identity):
    __tablename__   = PREFIX + 'iclamps'
    iclamp_key      = sqlalchemy.Column('iclamp_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True)
    experiment_key  = sqlalchemy.Column('experiment_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(PREFIX + 'experiments.experiment_key'))
    morphology_key  = sqlalchemy.Column('morphology_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(PREFIX + 'morphologies.morphology_key'))
    compartment_key = sqlalchemy.Column('compartment_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(PREFIX + 'compartments.compartment_key'))
    compartment_id  = sqlalchemy.Column('compartment_id',
        sqlalchemy.Integer)
    position        = sqlalchemy.Column('position', sqlalchemy.Float)
    amplitude       = sqlalchemy.Column('amplitude', sqlalchemy.Float)
    delay           = sqlalchemy.Column('delay', sqlalchemy.Float)
    duration        = sqlalchemy.Column('duration', sqlalchemy.Float)


class PatternClamp(mrj.model.clamp.PatternClamp, Identity):
    __tablename__   = PREFIX + 'vpatternclamps'
    patternclamp_key=   sqlalchemy.Column('patternclamp_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True)
    experiment_key  = sqlalchemy.Column('experiment_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(PREFIX + 'experiments.experiment_key'))
    morphology_key  = sqlalchemy.Column('morphology_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(PREFIX + 'morphologies.morphology_key'))
    compartment_key = sqlalchemy.Column('compartment_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(PREFIX + 'compartments.compartment_key'))
    compartment_id  = sqlalchemy.Column('compartment_id', sqlalchemy.Integer)
    position        = sqlalchemy.Column('position', sqlalchemy.Float)
    delta_t         = sqlalchemy.Column('delta_t', sqlalchemy.Float)
    delay           = sqlalchemy.Column('delay', sqlalchemy.Float)
    duration        = sqlalchemy.Column('duration', sqlalchemy.Float)


class Clamp_groups(mrj.util.auto_string.Auto_string, Identity):
    __tablename__   = PREFIX + 'iclamps_groups'
    iclamp_group_key= sqlalchemy.Column('iclamp_group_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True)
    name            = sqlalchemy.Column('name', sqlalchemy.String)
    description     = sqlalchemy.Column('description', sqlalchemy.String)
    voltagetrace_key= sqlalchemy.Column('voltagetrace_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(PREFIX + 'voltage_traces.voltagetrace_key'))
    morphology_key  = sqlalchemy.Column(
        sqlalchemy.ForeignKey(PREFIX + 'morphologies.morphology_key'))
    compartment_key = sqlalchemy.Column('compartment_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(PREFIX + 'compartments.compartment_key'))
    compartment_id  = sqlalchemy.Column('compartment_id', sqlalchemy.Integer)
    position        = sqlalchemy.Column('position', sqlalchemy.Float)
    amplitude       = sqlalchemy.Column('amplitude', sqlalchemy.Float)
    function        = sqlalchemy.Column('function', sqlalchemy.String)
    delta_t         = sqlalchemy.Column('delta_t', sqlalchemy.Float)
    delay           = sqlalchemy.Column('delay', sqlalchemy.Float)
    duration        = sqlalchemy.Column('duration', sqlalchemy.Float)


class Clamps_clamp_groups_map(Base):
    __tablename__   = PREFIX + 'clamps_clamp_groups_map'
    iclamp_key      = sqlalchemy.Column('iclamp_key',
        None,
        sqlalchemy.ForeignKey(PREFIX + 'iclamps.iclamp_key'),
        sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True)
    iclamp_group_key= sqlalchemy.Column('iclamp_group_key',
        None,
        sqlalchemy.ForeignKey(PREFIX + 'iclamps_groups.iclamp_group_key'),
        sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True)
