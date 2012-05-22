# -*- coding: utf-8 -*-
import sqlalchemy
from datajongleur import Base
from datajongleur.beanbags.models import PREFIX as BB_PREFIX
from datajongleur.beanbags.models import *
import mrj.model.sinusresult
import mrj.util.pattern_generator


PREFIX = 'mrj_'

class SinusResult_old(mrj.model.sinusresult.SinusResult, Identity):
    __tablename__   = PREFIX + 'sinusresult'
    uuid = sa.Column(
        sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True
    )
    #morphology_key  = sqlalchemy.Column('morphology_key', sqlalchemy.Integer)   #, sqlalchemy.ForeignKey(PREFIX + '_morphologies.morphology_key')
    morphology_name  = sqlalchemy.Column('morphology_name', sqlalchemy.String)
    compartment_id  = sqlalchemy.Column('compartment_id', sqlalchemy.Integer)
    #morphology = voltage_trace.morphology
    #compartment= compartment
    frequency       = sqlalchemy.Column('frequency', sqlalchemy.Float)
    maximum         = sqlalchemy.Column('maximum', sqlalchemy.Float)
    minimum         = sqlalchemy.Column('minimum', sqlalchemy.Float)
    phase_angle     = sqlalchemy.Column('phase_angle', sqlalchemy.Float)


class SinusResult(mrj.model.sinusresult.SinusResult, Identity):
    __tablename__   = PREFIX + 'sinusresults'
    uuid = sa.Column(
        sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True
    )
    morphology_name = sqlalchemy.Column('morphology_name', sqlalchemy.String),#TODO: remove
    frequency       = sqlalchemy.Column('frequency', sqlalchemy.Float),

    sinusresult_key = sqlalchemy.Column('sinusresult_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'), primary_key=True)
    voltagetrace_key= sqlalchemy.Column('voltagetrace_key',  sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'voltage_traces.voltagetrace_key'))
    sinusexperiment_key = sqlalchemy.Column('sinusexperiment_key',  sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'sinusexperiments.sinusexperiment_key'))
    v_max           = sqlalchemy.Column('v_max', sqlalchemy.Float)
    t_max           = sqlalchemy.Column('t_max', sqlalchemy.Float)
    v_min           = sqlalchemy.Column('v_min', sqlalchemy.Float)
    t_min           = sqlalchemy.Column('t_min', sqlalchemy.Float)
    delay           = sqlalchemy.Column('delay', sqlalchemy.Float)
    _phase_angle     = sqlalchemy.Column('_phase_angle', sqlalchemy.Float)


class SinusClamp(mrj.util.pattern_generator.SinusClamp, Identity):
    __tablename__   = PREFIX + 'sinusclamps'
    uuid = sa.Column(
        sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True
    )
    iclamp_key      =   sqlalchemy.Column('iclamp_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'), primary_key=True),
    voltagetrace_key= sqlalchemy.Column('voltagetrace_key',  sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'voltage_traces.voltagetrace_key')),
    morphology_key  = sqlalchemy.Column('morphology_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'morphologies.morphology_key')),
    compartment_key = sqlalchemy.Column('compartment_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'compartments.compartment_key')),
    compartment_id  = sqlalchemy.Column('compartment_id', sqlalchemy.Integer),
    position        = sqlalchemy.Column('position', sqlalchemy.Float),
    amplitude       = sqlalchemy.Column('amplitude', sqlalchemy.Float),
    delta_t         = sqlalchemy.Column('delta_t', sqlalchemy.Float),
    delay           = sqlalchemy.Column('delay', sqlalchemy.Float),
    duration        = sqlalchemy.Column('duration', sqlalchemy.Float)
