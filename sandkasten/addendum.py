__author__ = 'philipp'

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
from datajongleur.utils.sa import UUID, UUIDMixin

PREFIX = ""
BB_PREFIX = ""

Base = declarative_base()

addendum_addendum_maps = sa.Table(
    PREFIX + 'addendum_addendum_maps',
    Base.metadata,
    sa.Column(
        'addendum_uuid',
        sa.ForeignKey(PREFIX + 'addenda.uuid')),
    sa.Column(
        'addendum_ref_uuid',
        sa.ForeignKey(PREFIX + 'addenda.uuid')),
    sa.UniqueConstraint('addendum_uuid', 'addendum_ref_uuid'),
)


class Addendum(UUIDMixin, Base):
    __tablename__ = PREFIX + 'addenda'
    __table_args__ = (
        sa.UniqueConstraint('name', 'uuid'),
            {}
        )
    uuid = UUIDMixin.uuid
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String)
    flag = sa.Column(
        sa.Boolean,
        nullable=False,
        default=False) # PR: better on DB-Level

    def __init__(self, name='', description='', flag=False, badges=None):
        self.name = name
        self.description = description
        self.flag = flag
        if badges is not None:
            self.badges = badges

    references_to = orm.relationship(
        'Addendum',
        secondary=addendum_addendum_maps,
        primaryjoin=uuid == addendum_addendum_maps.c.addendum_uuid,
        secondaryjoin=uuid == addendum_addendum_maps.c.addendum_ref_uuid,
        #        foreign_keys=[
        #            addendum_addendum_maps.c.addendum_uuid,
        #            addendum_addendum_maps.c.addendum_ref_uuid],
        backref='referenced_from')


if __name__ == "__main__":
  engine = sa.create_engine('sqlite:///:memory:', echo=True)
  Session = orm.sessionmaker(bind=engine)
  Base.metadata.create_all(engine)
  session = Session()
  a = Addendum(name="Philipp", description="kleiner Test", flag=True)