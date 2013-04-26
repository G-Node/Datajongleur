__author__ = 'philipp'
import datetime as dt

import sqlalchemy as sa
import sqlalchemy.orm as orm

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.hybrid import hybrid_property

from utils import add_caption_date_name, now_as_string

Base = declarative_base()


##############
# Domain-Model
##############
@add_caption_date_name
class GeneralContainer(Base):
    __tablename__ = "general_containers"
    id = sa.Column(sa.Integer, primary_key=True)
    date = sa.Column(sa.String, default=now_as_string)
    name = sa.Column(sa.String, unique=True)
    __table_args__ = (
        sa.UniqueConstraint(name, date),
        {})

    # Properties:
    dict_of_specific_other_containers = orm.relationship(
        "SpecificOtherContainer",
        collection_class=attribute_mapped_collection('__caption__'),
        viewonly=True)

    dict_of_specific_containers = orm.relationship(
        "SpecificContainer",
        collection_class=attribute_mapped_collection('__caption__'),
        viewonly=True)


@add_caption_date_name
class SpecificContainer(Base):
    __tablename__ = "specific_containers"
    id = sa.Column(sa.Integer, primary_key=True)
    general_container_id = sa.Column(sa.Integer, sa.ForeignKey("general_containers.id"))
    date = sa.Column(sa.String, default=now_as_string)
    name = sa.Column(sa.String)
    par1 = sa.Column(sa.Float)
    content = sa.Column(sa.Text)
    __table_args__ = (
        sa.UniqueConstraint(date, name),
        {})

    general_container = orm.relationship("GeneralContainer", backref="specific_containers")
    dict_of_data = orm.relationship(
        "Data",
        collection_class=attribute_mapped_collection('__caption__'),
        viewonly=True)

@add_caption_date_name
class SpecificOtherContainer(Base):
    __tablename__ = "specific_other_containers"
    id = sa.Column(sa.Integer, primary_key=True)
    general_container_id = sa.Column(sa.Integer, sa.ForeignKey("general_containers.id"))
    date = sa.Column(sa.String, default=now_as_string)
    name = sa.Column(sa.String)
    par2 = sa.Column(sa.Integer)
    content = sa.Column(sa.Text)
    __table_args__ = (
        sa.UniqueConstraint(date, name),
        {})

    # Properties:
    # general_container = orm.relationship("GeneralContainer", backref="specific_other_containers")
    # dict_of_data = orm.relationship(
    #     "Data",
    #     collection_class=attribute_mapped_collection('__caption__'),
    #     viewonly=True)

class Data(Base):
    __tablename__ = "datas"
    id = sa.Column(sa.Integer, primary_key=True)
    specific_container_id = sa.Column(sa.Integer, sa.ForeignKey("specific_containers.id"))
    name = sa.Column(sa.String, unique=True)
    date = sa.Column(sa.String, default=now_as_string)
    content = sa.Column(sa.Text)
    __table_args__ = (
        sa.UniqueConstraint(specific_container_id, name),
        {})

    specific_container = orm.relationship("SpecificContainer", backref="datas")

    @property
    def __caption__(self):
        return self.name


# engine = sa.create_engine('sqlite:///:memory:', echo=True)
engine = sa.create_engine('sqlite:///test.sqlite', echo=False)
Session = orm.sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()

if __name__ == "__main__":
    if False:
        import inspect
        print inspect.getclasstree([GeneralContainer, SpecificContainer, Data])

    if True:
        # Check relationships
        gc = GeneralContainer(name="GContainer-1")
        session.add(gc)
        session.commit()

        sc = SpecificContainer(name="SContainer-1")
        gc.specific_containers.append(sc)
        session.commit()

        data = Data(name="Data-1")
        sc.datas.append(data)
        session.commit()

        # Check composite type
        # caption = DateNameCaption.newByCaption("2013-04-19__PR-Test")
        caption = "2013-04-19__PR-Test"
        gc1= GeneralContainer(caption=caption)
        # gc1= GeneralContainer(caption=DateNameCaption(dt.datetime.now().date(), "Test"))
        session.add(gc1)
        session.commit()

        # Check captions
        # gc1 = GeneralContainer(caption=DateNameCaption.newByCaption("2013-04-05__Philipp"))
        gc1 = GeneralContainer(caption="2013-04-05__Philipp")
        session.add(gc1)
        session.commit()

        # Check
        gc.specific_other_containers.append(SpecificOtherContainer(caption="2013-01-01__KleinerTestt"))
        session.commit()

        soc = gc.dict_of_specific_other_containers['2013-01-01__KleinerTestt']
