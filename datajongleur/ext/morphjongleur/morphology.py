# -*- coding: utf-8 -*-
'''
@author: stransky
@see neo.models
'''
#http://www.sqlalchemy.org/docs/orm/mapper_config.html
import sqlalchemy.orm #from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from datajongleur import Base
from datajongleur.beanbags.models import PREFIX as BB_PREFIX
from datajongleur.beanbags.models import *
import mrj.model.morphology
import mrj.util.auto_string

PREFIX = 'mrj_'

class Compartment(mrj.model.morphology.Compartment, Identity):
        #compartment_view_auto   = sqlalchemy.Table(PREFIX + 'compartments', self.metadata, autoload=True, autoload_with=self.engine)
        __tablename__ = PREFIX + 'compartments'
        compartment_key = sa.Column(
            #'compartment_key',
            sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
            #sqlalchemy.Integer, 
            primary_key=True
        )
        morphology_key  = sqlalchemy.Column('morphology_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'morphologies.morphology_key'))
        compartment_id  = sqlalchemy.Column('compartment_id', sqlalchemy.Integer)
        compartment_parent_id   = sqlalchemy.Column('compartment_parent_id', sqlalchemy.Integer)
        radius          = sqlalchemy.Column('radius', sqlalchemy.Float)
        x   = sqlalchemy.Column('x', sqlalchemy.Float)
        y   = sqlalchemy.Column('y', sqlalchemy.Float)
        z   = sqlalchemy.Column('z', sqlalchemy.Float)

class Compartment_info(mrj.util.auto_string.Auto_string, Identity):
        """
 parent_radius          = %f,
 length                 = %f,
 cylindric_volume       = %f,
 cylindric_lateral_area = %f,
   frustum_length       = %f,
   frustum_volume       = %f,
   frustum_lateral_area = %f,
 #children              = %i
        """
        __tablename__ = PREFIX + 'v_compartments'
        compartment_key = sa.Column(
            sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
            sqlalchemy.ForeignKey(PREFIX + 'compartments.compartment_key'),
            primary_key=True
        )
        morphology_key  = sqlalchemy.Column('morphology_key', sqlalchemy.Integer, sqlalchemy.ForeignKey(PREFIX + 'v_morphologies_metric_surface_area.morphology_key'))
        compartment_id  = sqlalchemy.Column('compartment_id', sqlalchemy.Integer)
        compartment_parent_id   = sqlalchemy.Column('compartment_parent_id', sqlalchemy.Integer) 
        radius          = sqlalchemy.Column('radius', sqlalchemy.Float)
        x               = sqlalchemy.Column('x', sqlalchemy.Float)
        y               = sqlalchemy.Column('y', sqlalchemy.Float)
        z               = sqlalchemy.Column('z', sqlalchemy.Float)
        parent_radius   = sqlalchemy.Column('parent_radius', sqlalchemy.Float)
        parent_x        = sqlalchemy.Column('parent_x', sqlalchemy.Float)
        parent_y        = sqlalchemy.Column('parent_y', sqlalchemy.Float)
        parent_z        = sqlalchemy.Column('parent_z', sqlalchemy.Float)
        length          = sqlalchemy.Column('length', sqlalchemy.Float)
        frustum_length  = sqlalchemy.Column('frustum_length', sqlalchemy.Float)
        frustum_volume  = sqlalchemy.Column('frustum_volume', sqlalchemy.Float)
        frustum_lateral_area    = sqlalchemy.Column('frustum_lateral_area', sqlalchemy.Float) 
        cylindric_volume        = sqlalchemy.Column('cylindric_volume', sqlalchemy.Float)
        cylindric_lateral_area  = sqlalchemy.Column('cylindric_lateral_area', sqlalchemy.Float)
        children        = sqlalchemy.Column('children', sqlalchemy.Integer)

#        _compartment    =   sqlalchemy.orm.relation(Compartment, backref='_info')

class Compartment_groups(mrj.util.auto_string.Auto_string, Identity):
        __tablename__ = PREFIX + 'compartment_groups'
        compartment_group_key = sa.Column(
            #'compartment_group_key',
            sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
            #sqlalchemy.Integer, 
            primary_key=True
        )
        name    = sqlalchemy.Column('name', sqlalchemy.String)
        description = sqlalchemy.Column('description', sqlalchemy.String)
        type    = sqlalchemy.Column('type', sqlalchemy.String)
        
        _compartment  =   sqlalchemy.orm.relation(Compartment, secondary=PREFIX + 'compartments_compartment_groups_map', backref='_groups')
            
class Compartments_compartment_groups_map(Base):         
        __tablename__ = PREFIX + 'compartments_compartment_groups_maps'
        compartment_key = sqlalchemy.Column('compartment_key', None, sqlalchemy.ForeignKey(PREFIX + 'compartments.compartment_key'), primary_key=True)
        compartment_group_key   = sqlalchemy.Column('compartment_group_key', None, sqlalchemy.ForeignKey(PREFIX + 'compartment_groups.compartment_group_key'), primary_key=True)


class Morphology(mrj.model.morphology.Morphology, Identity):
        #morphology_view_auto    = sqlalchemy.Table(PREFIX + 'v_morphologies_metric_surface_area', self.metadata, autoload=True, autoload_with=self.engine)
        #morphology_view_auto    = sqlalchemy.Table(PREFIX + 'morphologies', self.metadata, autoload=True, autoload_with=self.engine)    
        __tablename__ = PREFIX + 'morphologies'
        morphology_key = sa.Column(
            #'morphology_key',
            sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
            #sqlalchemy.Integer, 
            primary_key=True
        )
        name        = sqlalchemy.Column('name', sqlalchemy.String)
        file_origin = sqlalchemy.Column('file_origin', sqlalchemy.String)
        description = sqlalchemy.Column('description', sqlalchemy.String)
        #sqlalchemy.Column('datetime_insert', sqlalchemy.String)
        datetime_recording  = sqlalchemy.Column('datetime_recording', sqlalchemy.String)
    
        #_compartments=sqlalchemy.orm.relationship(mrj.dj.morphology.Compartment, backref='_morphology') }
        compartments    = sqlalchemy.orm.relation(Compartment, backref='_morphology')
#       mrj_experiments= sqlalchemy.orm.relation(Experiment, primaryjoin= self.morphology_table.c.morphology_key == self.experiment_table.c.morphology_key )

class Morphology_info(mrj.util.auto_string.Auto_string, Identity):
        """
    path_length         = %f, 
 surface_length         = %f, 
 cylindric_volume       = %f, 
   frustum_volume       = %f, 
 cylindric_lateral_area = %f, 
   frustum_lateral_area = %f, 
 cylindric_surface_area = %f, 
   frustum_surface_area = %f, 
 #branches              = %i
        """
        __tablename__ = PREFIX + 'v_morphologies_metric_surface_area'
        morphology_key = sa.Column(
            #'morphology_key',
            sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
            sqlalchemy.ForeignKey(PREFIX + 'morphologies.morphology_key'),
            #sqlalchemy.Integer, 
            primary_key=True
        )
        name            = sqlalchemy.Column('name', sqlalchemy.String)
        file_origin     = sqlalchemy.Column('file_origin', sqlalchemy.String)
        description     = sqlalchemy.Column('description', sqlalchemy.String)
        datetime_insert = sqlalchemy.Column('datetime_insert', sqlalchemy.String)
        datetime_recording  = sqlalchemy.Column('datetime_recording', sqlalchemy.String)
        path_length     = sqlalchemy.Column('path_length', sqlalchemy.Float)
        surface_length  = sqlalchemy.Column('surface_length', sqlalchemy.Float) 
        cylindric_volume    = sqlalchemy.Column('cylindric_volume', sqlalchemy.Float)
        frustum_volume  = sqlalchemy.Column('frustum_volume', sqlalchemy.Float)
        cylindric_lateral_area  = sqlalchemy.Column('cylindric_lateral_area', sqlalchemy.Float)
        frustum_lateral_area    = sqlalchemy.Column('frustum_lateral_area', sqlalchemy.Float)
        cylindric_surface_area  = sqlalchemy.Column('cylindric_surface_area', sqlalchemy.Float)
        frustum_surface_area    = sqlalchemy.Column('frustum_surface_area', sqlalchemy.Float)
        cylindric_mcse          = sqlalchemy.Column('cylindric_mcse', sqlalchemy.Float)
        frustum_mcse            = sqlalchemy.Column('frustum_mcse', sqlalchemy.Float)
        compartments            = sqlalchemy.Column('compartments', sqlalchemy.Integer)
        leafs                   = sqlalchemy.Column('leafs', sqlalchemy.Integer)
        branches                = sqlalchemy.Column('branches', sqlalchemy.Integer)
        age                     = sqlalchemy.Column('age', sqlalchemy.Integer)
        axon                    = sqlalchemy.Column('axon', sqlalchemy.String)

        _morphology             = sqlalchemy.orm.relation(Morphology, backref='_info')

class Morphology_groups(mrj.util.auto_string.Auto_string, Identity):
        __tablename__ = PREFIX + 'morphology_groups'
        morphology_group_key  = sa.Column(
            #'morphology_group_key ',
            sqlalchemy.ForeignKey(BB_PREFIX + 'identities.uuid'),
            #sqlalchemy.Integer, 
            primary_key=True
        )
        name        = sqlalchemy.Column('name', sqlalchemy.String)
        description = sqlalchemy.Column('description', sqlalchemy.String)
        age         = sqlalchemy.Column('age', sqlalchemy.Float)

        _morphology = sqlalchemy.orm.relation(Morphology, secondary=PREFIX + 'morphologies_morphology_groups_map', backref='_groups')
    
class Morphologies_morphology_groups_map(Base):
        __tablename__ = PREFIX + 'morphologies_morphology_groups_maps'
        morphology_key          = sqlalchemy.Column('morphology_key', None, sqlalchemy.ForeignKey(PREFIX + 'morphologies.morphology_key'), primary_key=True)
        morphology_group_key    = sqlalchemy.Column('morphology_group_key', None, sqlalchemy.ForeignKey(PREFIX + 'morphology_groups.morphology_group_key'), primary_key=True)
