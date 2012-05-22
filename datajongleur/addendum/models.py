import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.collections import attribute_mapped_collection
import sqlamp
import uuid
from datajongleur import Base, DBSession
from datajongleur import declarative_base
from datajongleur.beanbags.models import PREFIX as BB_PREFIX
from datajongleur.utils.sa import UUID, UUIDMixin

PREFIX = "addendum_"
BaseNode = declarative_base(metadata=Base.metadata,
                            metaclass=sqlamp.DeclarativeMeta)

addendum_addendum_maps = sa.Table(
    PREFIX + 'addendum_addendum_maps',
    Base.metadata,
    sa.Column (
      'addendum_uuid',
      sa.ForeignKey (PREFIX + 'addenda.uuid')),
    sa.Column (
      'addendum_ref_uuid',
      sa.ForeignKey (PREFIX + 'addenda.uuid')),
    sa.UniqueConstraint('addendum_uuid', 'addendum_ref_uuid'),
    )
"""
sa.ForeignKeyConstraint(
  ['addendum_uuid'],
  [PREFIX + 'addenda.uuid']),
sa.ForeignKeyConstraint(
  ['addendum_ref_uuid'],
  [PREFIX + 'addenda.uuid']),
"""


class Addendum(UUIDMixin, Base):
  __tablename__ = PREFIX + 'addenda'
  __table_args__ = (
      sa.UniqueConstraint('name', 'uuid'),
      {}
      )
  name = sa.Column (sa.String, nullable=False)
  description = sa.Column (sa.String)
  flag = sa.Column (
      sa.Boolean,
      nullable=False,
      default=False) # PR: better on DB-Level
  identity_uuid = sa.Column (
      sa.ForeignKey (BB_PREFIX + 'identities.uuid',),
      unique=True
      )

  def __init__(self, name='', description='', flag=False, badges=None):
    self.name = name
    self.description = description
    self.flag = flag
    if badges is not None:
      self.badges = badges

  identity = orm.relationship(
      "Identity",
      backref=orm.backref('addendum', uselist=False)
      )

  badges = association_proxy (
      'addendum_badge_maps',
      'badge_value',
      creator=lambda bt, bv:
        AddendumBadgeMap(badge_type=bt, badge_value=bv)
      )

  references_to = orm.relationship(
      'Addendum',
      secondary=addendum_addendum_maps,
      primaryjoin=\
          'uuid'==addendum_addendum_maps.c.addendum_uuid,
      secondaryjoin=\
          'uuid'==addendum_addendum_maps.c.addendum_ref_uuid,
      foreign_keys=[
        addendum_addendum_maps.c.addendum_uuid,
        addendum_addendum_maps.c.addendum_ref_uuid],
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
    return """%s(name=%r, description=%r, flag=%r)""" %(
        self.__class__.__name__,
        self.name,
        self.description,
        self.flag
        )


class ATreeNode(BaseNode):
  __tablename__ = PREFIX + 'a_tree_nodes'
  __table_args__ = (
      sa.ForeignKeyConstraint(
        ['name', 'addendum_uuid'],
        [PREFIX + 'addenda.name', PREFIX + 'addenda.uuid']),
      sa.ForeignKeyConstraint(
        ['parent_node_key'],
        [PREFIX + 'a_tree_nodes.node_key']
        ),
      {})
  __mp_manager__ = 'mp'

  # Attributes
  node_key = sa.Column(sa.Integer, primary_key=True)
  parent_node_key = sa.Column(
      sa.Integer,
      #sa.ForeignKey(PREFIX + 'a_tree_nodes.node_key')
      )
  name = sa.Column(sa.String)#, sa.ForeignKey('addenda.name'))
  addendum_uuid = sa.Column(UUID)
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


class AddendumBadgeMap(Base):
  __tablename__ = PREFIX + 'addendum_badge_maps'
  __table_args__ = (
      sa.PrimaryKeyConstraint('key'),
      sa.UniqueConstraint('badge_uuid', 'badge_type'),
      {}
      )
  key = sa.Column('key', sa.Integer)
  addendum_uuid = sa.Column('addendum_uuid',
      sa.ForeignKey(PREFIX + 'addenda.uuid'), nullable=False)
  badge_uuid =  sa.Column('badge_uuid',
      sa.ForeignKey(PREFIX + 'badges.uuid'), nullable=False)
  badge_type = sa.Column (sa.String)

  # Properties
  addendum = orm.relationship(Addendum, backref=orm.backref(
      'addendum_badge_maps',
      collection_class = attribute_mapped_collection("badge_type"),
      cascade="all, delete-orphan")
    )

  badge = orm.relationship('Badge',
      single_parent=True,
      #cascade="all, delete-orphan"
      )

  badge_value = association_proxy ('badge', 'value')


class Badge(UUIDMixin, Base):
  __tablename__ = PREFIX + 'badges'
  value = sa.Column (sa.String)

  def __init__(self, value):
    self.value = value

  def __repr__(self):
    return "%s(badge_type=%r, value=%r)" %(
        self.__class__.__name__,
        self.value)


def glue_to_addendum(cls):
  addendum_type_two_maps = get_glue_addenda_table(cls, 'glue_addenda_')
  cls.metadata.create_all ()
  cls.addendum = orm.relationship(
      'Addendum',
      secondary=addendum_type_two_maps,
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
          self._addendum = Addendum(name=value, description='', flag=False)
        else:
          dto = self.__dict__[dto_name]
          dto._addendum = Addendum(name=value, description='', flag=False)

    cls.name = property(getName, setName)
    cls.getName = getName
    cls.setName = setName
    return cls
  return decorateClass
