from datajongleur import Base, declarative_base
import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlamp
import uuid
from datajongleur.utils.sa import NumpyType, GUID

PREFIX = "beanbag_"

BaseNode = declarative_base(metadata=Base.metadata,
                            metaclass=sqlamp.DeclarativeMeta)

##########
# Quantity
##########

class DTOQuantity(Base):
  __tablename__ = PREFIX + 'quantities'

  key = sa.Column('key', sa.Integer, primary_key=True)
  uuid = sa.Column('uuid', GUID, unique=True,
      default=uuid.uuid4)
  amount = sa.Column('amount', NumpyType)
  units = sa.Column('units', sa.String)


##########
# Addendum
##########

addendum_badge_maps = sa.Table(
    PREFIX + 'addendum_badge_maps',
    Base.metadata,
    sa.Column(
      'addendum_key', sa.Integer, sa.ForeignKey(
        PREFIX + 'addenda.addendum_key')),
    sa.Column('badge_key', sa.ForeignKey(PREFIX + 'badges.badge_key')),
    )

addendum_addendum_maps = sa.Table(
    PREFIX + 'addendum_addendum_maps',
    Base.metadata,
    sa.Column (
      'addendum_key',
      sa.Integer,
      sa.ForeignKey (PREFIX + 'addenda.addendum_key')),
    sa.Column (
      'addendum_ref_key',
      sa.Integer,
      sa.ForeignKey (PREFIX + 'addenda.addendum_key')),
    #sa.UniqueConstraint('addendum_key', 'addendum_ref_key')
    )


class Addendum(Base):
  __tablename__ = PREFIX + 'addenda'

  addendum_key = sa.Column (sa.Integer, primary_key=True)
  name = sa.Column (sa.String, nullable=False)
  description = sa.Column (sa.String)
  flag = sa.Column (
      sa.Boolean,
      nullable=False,
      default=False) # PR: better on DB-Level

  _list_of_addendees = []

  references_to = orm.relationship(
      'Addendum',
      secondary=addendum_addendum_maps,
      primaryjoin=addendum_key==addendum_addendum_maps.c.addendum_key,
      secondaryjoin=addendum_key==addendum_addendum_maps.c.addendum_ref_key,
      backref='referenced_from')

  def getChildren(self):
    return [a_tree_node.addendum for a_tree_node in self.a_tree_nodes.children]

  children = property(getChildren)

  @classmethod
  def _append_list_of_addendees(cls, addendee_name):
    cls._list_of_addendees.append(addendee_name)

  @classmethod
  def _get_list_of_addendees(cls):
    return cls._list_of_addendees

  def getAddendee(self):
    addendees = []
    for addendee in self._get_list_of_addendees():
      if addendee is not None:
        addendees.append(addendee)
    assert len(addendees) < 2, "More than one addendees assigned."
    if len(addendees) == 1:
      return self.__getattribute__("_"+addendees[0])
    else:
      return None
  def setAddendee(self, obj):
    
    self.__setattr__("_" + obj.__class__.__name__, obj)
  addendee = property(getAddendee, setAddendee)

  def addBadge(self, badge_type, value):
    badge = Badge(badge_type=badge_type, value=value)
    self.badges.append(badge)

  def __repr__(self):
    return """%s(name=%r, description=%r, favorite=%r)""" %(
        self.__class__.__name__,
        self.name,
        self.description,
        self.favorite
        )


class ATreeNode(BaseNode):
  __tablename__ = PREFIX + 'a_tree_nodes'
  __table_args__ = (sa.ForeignKeyConstraint(
      ['name', 'addendum_key'],
      [PREFIX + 'addenda.name', PREFIX + 'addenda.addendum_key']),
      {})
  __mp_manager__ = 'mp'

  # Attributes
  node_key = sa.Column(sa.Integer, primary_key=True)
  parent_node_key = sa.Column(
      sa.Integer,
      sa.ForeignKey(PREFIX + 'a_tree_nodes.node_key'))
  name = sa.Column(sa.String)#, sa.ForeignKey('addenda.name'))
  addendum_key = sa.Column(sa.Integer)
  # Properties
  addendum = orm.relationship(
      Addendum, backref="a_tree_nodes")
  children = orm.relationship('ATreeNode',
      cascade="all, delete",
      backref=orm.backref("parent", remote_side='ATreeNode.node_key'),
      )

  def __init__(self, addendum, parent=None):
    self.addendum = addendum
    self.parent = parent

  def append(self, addendum):
    self.children.append(ATreeNode(addendum, parent=self))

  def __repr__(self):
    return "%s(name=%r, node_key=%r, parent_node_key=%r)" % (
        self.__class__.__name__,
        self.addendum,
        self.node_key,
        self.parent_node_key
        )


class Badge(Base):
  __tablename__ = PREFIX + 'badges'
  __table_args__ = (
      sa.PrimaryKeyConstraint('badge_key'),
      #sa.UniqueConstraint('badge_type', 'value'),
      {}
      )
  badge_key = sa.Column (sa.Integer)
  badge_type = sa.Column (sa.String)
  value = sa.Column (sa.String)

  addenda = orm.relationship (
      'Addendum',
      secondary=addendum_badge_maps,
      backref='badges')

  def __repr__(self):
    return "%s(badge_type=%r, value=%r)" %(
        self.__class__.__name__,
        self.badge_type,
        self.value)


def glue_to_addendum(cls):
  addendum_object_type_two_maps = get_glue_addenda_table(cls, 'glue_addenda_')
  cls.metadata.create_all ()
  cls.addendum = orm.relationship(
      'Addendum',
      secondary=addendum_object_type_two_maps,
      backref=orm.backref(
        '_' + cls.__name__,
        uselist=False), # PR: Just for `getting`, not `setting`.
      uselist=False)
  Addendum._append_list_of_addendees(cls.__name__)

def dump_atree(node, indent=0):
  return "   " * indent + repr(node) + \
              "\n" + \
              "".join([
                  dump_atree(c, indent +1) 
                  for c in node.children])

def addSpecificBadgeViaAddendum(badge_type, addendum_name='_addendum'):
  def decorateClass(cls):
    def getAddendum(self):
      return self.__getattribute__(addendum_name)
    def getBadgesOfType(self):
      addendum = getAddendum(self)
      badges = addendum.badges
      badges_of_type = []
      for badge in badges:
        if badge.badge_type == badge_type:
          badges_of_type.append(badge)
      return badges_of_type

    def getBadge(self):
      addendum = getAddendum(self)
      badges = addendum.badges
      values = []
      for badge in badges:
        if badge.badge_type == badge_type:
          values.append(badge.value)
      if len(values) == 1: return values[0]
      if len(values) == 0: return None
      raise AttributeError, 'More than one %s assiged!' %(badge_type)
    def setBadge(self, value):
      badges_of_type = getBadgesOfType(self)
      if len(badges_of_type) == 1:
        badges_of_type[0].value = value
        return
      if len(badges_of_type) == 0:
        addendum = getAddendum(self)
        addendum.badges.append(Badge(badge_type=badge_type, value=value))
        return
      raise AttributeError, 'More than one %s assiged!' %(badge_type)
    setattr(cls, badge_type, property(getBadge, setBadge))
    return cls
  return decorateClass

def addAddendumAccess(dto_name):
  def decorateClass(cls):
    def getName(self):
      try:
        return self._addendum.name
      except AttributeError, e:
        return ""

    def setName(self, value):
      try:
        self._addendum.name = value
      except AttributeError, e:
        if not dto_name:
          self._addendum = Addendum(name=value, description='', favorite=False)
        else:
          dto = self.__dict__[dto_name]
          dto._addendum = Addendum(name=value, description='', favorite=False)

    cls.name = property(getName, setName)
    cls.getName = getName
    cls.setName = setName
    return cls
  return decorateClass
