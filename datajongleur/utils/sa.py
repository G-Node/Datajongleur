import numpy as np
import zlib
import uuid

import sqlalchemy as sa
from sqlalchemy.orm.util import has_identity

from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid

from datajongleur import DBSession

class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value)
            else:
                # hexstring
                return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)

class NumpyType (sa.types.TypeDecorator):
  impl = sa.types.LargeBinary

  def process_bind_param(self, value, dialect):
    return zlib.compress(value.dumps(), 9)

  def process_result_value(self, value, dialect):
    return np.loads(zlib.decompress(value))


class NumpyTypePGSpecific (sa.types.TypeDecorator):
  """
  see `<http://www.sqlalchemy.org/docs/core/types.html>`_
  """
  impl = sa.types.LargeBinary

  def load_dialect_impl(self, dialect):
    if dialect.name == 'postgresql':
      return dialect.type_descriptor(ARRAY(sa.Float))
    else:
      return dialect.type_descriptor(sa.types.LargeBinary)

  def process_bind_param(self, value, dialect):
    """
    not adjusted yet
    """
    return zlib.compress(value.dumps(), 9)

  def process_result_value(self, value, dialect):
    """
    not adjusted yet
    """
    return np.loads(zlib.decompress(value))

#######################
## Decorators        ##

def getSession():
  return DBSession()

def passAttrDTO(cls):
  def genGetMyAttr(attr_name):
    def getMyAttr(self):
      try:
        dto = self.getDTO()
        if has_identity(dto):
          return getattr(self.getDTO(), attr_name)
        return
      except Exception, e:
        print Exception
        print e
    return getMyAttr
  cls.getKey = genGetMyAttr('key')
  cls.key = property(cls.getKey)
  cls.getUUID = genGetMyAttr('uuid')
  cls.uuid = property(cls.getUUID)
  return cls

def addInfoQuantityDBAccess():
  """
  This decorator adds the following methods:
  * ``load(PK)``
  * ``save()``
  """
  def decorateClass(cls):
    @classmethod
    def newBySession(cls, key):
      if not hasattr(cls, "_session"):
        cls.session = getSession()
      dto = cls.session.query(cls._DTO).filter(
          getattr(cls._DTO, 'key') == key).first()
      return cls.newByDTO(dto)
    @classmethod
    def load(cls, key):
      return cls.newBySession(key)
    def save(self):
      if not hasattr(self, "session"):
        self.__class__.session = getSession()
      dto = self.getDTO()
      key = self.getKey()
      self.session.add (dto)
      self.session.commit ()
      if key is not self.key:
        print "Assigned attribute ``key`` --> %r" % (self.key)
      
    cls.newBySession = newBySession
    cls.load = load
    cls.save = save
    return cls
  return decorateClass

## (end: Decorators) ##
#######################

def get_test_session(Base):
  engine = sa.create_engine ('sqlite:///test.sqlite', echo=False)
  Base.metadata.bind = engine
  Base.metadata.create_all ()
  session = DBSession ()
  return session
