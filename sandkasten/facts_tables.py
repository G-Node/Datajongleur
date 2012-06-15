"""
adjusted from http://stackoverflow.com/questions/1436011/star-schema-in-sqlalchemy
"""
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import instrument_declarative

class BaseMeta(type):
    classes = set()

    def __init__(cls, classname, bases, dict_):
        klass = type.__init__(cls, classname, bases, dict_)
        if 'metadata' not in dict_:
            BaseMeta.classes.add(cls)
        return klass


class Base(object):
    __metaclass__ = BaseMeta
    metadata = sa.MetaData()

    def __init__(self, **kw):
        for k in kw:
            setattr(self, k, kw[k])

    @classmethod
    def configure(cls, *klasses):
        registry = {}
        for c in BaseMeta.classes:
            instrument_declarative(c, registry, cls.metadata)


class Store(Base):
    __tablename__ = 'store'

    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.String(50), nullable=False)

    @classmethod
    def dimension(cls, target):
        target.store_id = sa.Column('store_id', sa.Integer, sa.ForeignKey('store.id'), primary_key=True)
        target.store = orm.relation(cls)
        return target


class Product(Base):
    __tablename__ = 'product'

    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.String(50), nullable=False)

    @classmethod
    def dimension(cls, target):
        target.product_id = sa.Column('product_id', sa.Integer, sa.ForeignKey('product.id'), primary_key=True)
        target.product = orm.relation(cls)
        return target


@Store.dimension
@Product.dimension
class FactOne(Base):
    __tablename__ = 'sales_fact_one'

    units_sold = sa.Column('units_sold', sa.Integer, nullable=False)


@Store.dimension
@Product.dimension
class FactTwo(Base):
    __tablename__ = 'sales_fact_two'

    units_sold = sa.Column('units_sold', sa.Integer, nullable=False)

Base.configure()

if __name__ == '__main__':
    engine = sa.create_engine('sqlite://', echo=True)
    Base.metadata.create_all(engine)

    sess = orm.sessionmaker(engine)()

    sess.add(FactOne(store=Store(name='s1'), product=Product(name='p1'), units_sold=27))
    sess.commit()