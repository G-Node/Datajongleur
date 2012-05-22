# -*- coding: utf-8 -*-
'''
@author: stransky
'''
import sqlalchemy.orm #from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import sqlalchemy.dialects.postgresql
from datajongleur import Base
from datajongleur.beanbags.models import PREFIX as BB_PREFIX
from datajongleur.beanbags.models import *
import mrj.model.experiment

PREFIX = 'mrj_'

class Experiment(mrj.model.experiment.Experiment, Identity):
    __tablename__   = PREFIX + 'experiments'
    experiment_key  = sqlalchemy.Column('experiment_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'), primary_key=True)
    uuid = experiment_key
    morphology_key  = sqlalchemy.Column('morphology_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'morphologies.morphology_key'))
#    iclamp_key      = sqlalchemy.Column('iclamp_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'iclamps.iclamp_key'))
    neuron_passive_parameter_key    = sqlalchemy.Column('neuron_passive_parameter_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'neuron_passive_parameters.neuron_passive_parameter_key'))
    nseg            = sqlalchemy.Column('nseg', sqlalchemy.Integer)
    description     = sqlalchemy.Column('description', sqlalchemy.String)

class RecordingPoint(mrj.model.experiment.RecordingPoint, Identity):
    __tablename__   = PREFIX + 'recordingpoints'
    recordingpoint_key  = sqlalchemy.Column('recordingpoint_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'), primary_key=True)
    uuid = recordingpoint_key
    experiment_key  = sqlalchemy.Column('experiment_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'experiments.experiment_key'))
    morphology_key  = sqlalchemy.Column('morphology_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'morphologies.morphology_key'))#redundant
    compartment_key = sqlalchemy.Column('compartment_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'compartments.compartment_key'))
    compartment_id  = sqlalchemy.Column('compartment_id', sqlalchemy.Integer)#redundant
    position        = sqlalchemy.Column('position', sqlalchemy.Float)

class VoltageTrace(mrj.model.experiment.VoltageTrace, Identity):
    __tablename__   = PREFIX + 'voltage_traces'
    voltagetrace_key= sqlalchemy.Column('voltagetrace_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'), primary_key=True)
    uuid = voltagetrace_key
    experiment_key  = sqlalchemy.Column('experiment_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'experiments.experiment_key'))
    recordingpoint_key  = sqlalchemy.Column('recordingpoint_key',  sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'recordingpoints.recordingpoint_key'))
    t               = sqlalchemy.Column('t', sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.Float))
    v               = sqlalchemy.Column('v', sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.Float))
    t_min           = sqlalchemy.Column('t_min', sqlalchemy.Float)
    v_min           = sqlalchemy.Column('v_min', sqlalchemy.Float)
    t_max           = sqlalchemy.Column('t_max', sqlalchemy.Float)
    v_max           = sqlalchemy.Column('v_max', sqlalchemy.Float)

class TauFit(mrj.model.experiment.TauFit, Identity):
    __tablename__   = PREFIX + 'tau_fits'
    tau_fit_key     = sqlalchemy.Column('tau_fit_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'), primary_key=True)
    uuid = tau_fit_key
    voltagetrace_key    = sqlalchemy.Column('voltagetrace_key',  sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'voltage_traces.voltagetrace_key'))
    experiment_key  = sqlalchemy.Column('experiment_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'experiments.experiment_key'))
    r_in            = sqlalchemy.Column('r_in', sqlalchemy.Float)
    tau_eff         = sqlalchemy.Column('tau_eff', sqlalchemy.Float)
    tau_eff_fit     = sqlalchemy.Column('tau_eff_fit', sqlalchemy.Float)
