import zlib
import sqlalchemy as sa
import sqlalchemy.orm as orm
import datetime as dt
from sqlalchemy import exc
from datajongleur.beanbags.models import *
from datajongleur import Base
from datajongleur.beanbags.models import PREFIX as BB_PREFIX

PREFIX = 'dj_admin_'


container_identities_map_table = sa.Table(
    PREFIX + "container_identitiy_maps", Base.metadata,
    sa.Column('uuid',
      sa.ForeignKey(BB_PREFIX + 'identities.uuid')),
    sa.Column('name', 
      sa.TEXT,
      sa.ForeignKey(PREFIX + 'beanbag_containers.name')),
    sa.PrimaryKeyConstraint('uuid', 'name'),
    )


class BeanbagContainer(Base):
  __tablename__ = PREFIX + 'beanbag_containers'
  name = sa.Column('name', sa.TEXT, primary_key=True)
  creation_time = sa.Column(
      'creation_time',
      sa.DateTime,
      default=dt.datetime.now())

  def __init__(self, name):
    self.name = name

  beanbags = orm.relationship(
      "Identity",
      secondary=container_identities_map_table,
      backref=orm.backref('containers'),
      )

  def __repr__(self):
    return "Container(%r)" %(self.name)


if __name__ == '__main__':
  pass
