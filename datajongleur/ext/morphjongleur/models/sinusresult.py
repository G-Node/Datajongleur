# -*- coding: utf-8 -*-
import sqlalchemy
from datajongleur import Base
from datajongleur.beanbags.models import PREFIX as BB_PREFIX
from datajongleur.beanbags.models import *
import mrj.model.sinusresult
import mrj.util.pattern_generator
from datajongleur.beanbags.models import Identity

PREFIX = 'mrj_'

class SinusResult_old(mrj.model.sinusresult.SinusResult, Identity):
    __tablename__   = PREFIX + 'sinusresult'
    uuid = sa.Column(
        sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True
    )
    morphology_name  = sqlalchemy.Column('morphology_name', sqlalchemy.String)
    compartment_id  = sqlalchemy.Column('compartment_id', sqlalchemy.Integer)
    frequency       = sqlalchemy.Column('frequency', sqlalchemy.Float)
    maximum         = sqlalchemy.Column('maximum', sqlalchemy.Float)
    minimum         = sqlalchemy.Column('minimum', sqlalchemy.Float)
    phase_angle     = sqlalchemy.Column('phase_angle', sqlalchemy.Float)


class SinusExperiment(mrj.model.sinusresult.SinusExperiment, Identity):
    __tablename__   = PREFIX + 'sinusexperiments'
    sinusexperiment_key = sqlalchemy.Column(
        sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True)
    experiment_key  = sqlalchemy.Column(
        sqlalchemy.ForeignKey('mrj_experiments.experiment_key'))
    frequency = sqlalchemy.Column('frequency', sqlalchemy.Float)


class SinusResult(mrj.model.sinusresult.SinusResult, Identity):
    __tablename__   = PREFIX + 'sinusresults'
    morphology_name = sqlalchemy.Column('morphology_name',
        sqlalchemy.String)#TODO: remove
    frequency       = sqlalchemy.Column('frequency', sqlalchemy.Float)
    sinusresult_key = sqlalchemy.Column('sinusresult_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True)
    voltagetrace_key= sqlalchemy.Column('voltagetrace_key',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(PREFIX + 'voltage_traces.voltagetrace_key'))
    sinusexperiment_key = sqlalchemy.Column(
        sqlalchemy.ForeignKey(PREFIX + 'sinusexperiments.sinusexperiment_key'))
    v_max           = sqlalchemy.Column('v_max', sqlalchemy.Float)
    t_max           = sqlalchemy.Column('t_max', sqlalchemy.Float)
    v_min           = sqlalchemy.Column('v_min', sqlalchemy.Float)
    t_min           = sqlalchemy.Column('t_min', sqlalchemy.Float)
    delay           = sqlalchemy.Column('delay', sqlalchemy.Float)
    _phase_angle     = sqlalchemy.Column('_phase_angle', sqlalchemy.Float)
