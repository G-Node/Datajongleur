# -*- coding: utf-8 -*-
'''
@author: stransky
'''
import sqlalchemy.orm #from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from datajongleur import Base
from datajongleur.beanbags.models import PREFIX as BB_PREFIX
from datajongleur.beanbags.models import *
import mrj.model.neuron_passive
from datajongleur.beanbags.models import Identity

PREFIX = 'mrj_'

class Neuron_passive_parameter(
    mrj.model.neuron_passive.Neuron_passive_parameter,
    Identity): 
    __tablename__   = PREFIX + 'neuron_passive_parameters'
    neuron_passive_parameter_key = sqlalchemy.Column(
        sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
        primary_key=True)
    Ra              = sqlalchemy.Column('Ra', sqlalchemy.Float)
    g               = sqlalchemy.Column('g', sqlalchemy.Float)
    e               = sqlalchemy.Column('e', sqlalchemy.Float)
