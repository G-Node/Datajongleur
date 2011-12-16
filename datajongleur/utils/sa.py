import numpy as np
import zlib
import sqlalchemy as sa
from datajongleur import DBSession

from sqlalchemy.types import TypeDecorator

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


def get_test_session(Base):
  engine = sa.create_engine ('sqlite:///test.sqlite', echo=False)
  Base.metadata.bind = engine
  Base.metadata.create_all ()
  session = DBSession ()
  return session
