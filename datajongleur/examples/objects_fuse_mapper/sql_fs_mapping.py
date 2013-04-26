__author__ = 'philipp'

import fuse
import stat
import errno
import os
import datetime
import calendar
import logging

from models import *

METADATA_FILENAMES = ['info.yaml', 'readme.rst']

####################################
# Required by ObjectFuseMapper (OFM)
####################################

class Nodeable(object):
    def __caption__(self):
        raise NotImplementedError
    def __subnodes__(self):
        raise NotImplementedError
    def __leafs__(self):
        raise NotImplementedError


    def __init__(self, caption, subnodes, leafs=None):
        """
        Example:

        >>> subnodes = {'caption1': node_1, 'caption_2': node_2}
        >>> leafs = {'leaf_1': leaf_1, 'leaf_2': leaf_2}
        >>> nodeable = Nodeable(subnodes, leafs}
        """
        self.__caption__ = caption
        self.__subnodes__ = subnodes
        if leafs == None:
            self.__leafs__ = {}
        else:
            self.__leafs__ = leafs


class Leafable(object):
    def __caption__(self):
        raise NotImplementedError
    def __content__(self):
        raise NotImplementedError


class Leaf(Leafable):
    def __init__(self, caption, content):
        self.__caption__ = caption
        self.__content__ = content


class Node(Nodeable):
    def __init__(self, caption, subnodes, leafs=None):
        """
        Example:

        >>> subnodes = {'caption1': node_1, 'caption_2': node_2}
        >>> leafs = {'leaf_1': leaf_1, 'leaf_2': leaf_2}
        >>> nodeable = Nodeable(subnodes, leafs}
        """
        self.__caption__ = caption
        self.__subnodes__ = subnodes
        if leafs == None:
            self.__leafs__ = {}
        else:
            self.__leafs__ = leafs


######################
# Generate Object Tree
######################

# Facade
class ObjectTree(object):
    def __init__(self):
        self.setup_treeobjects()
        self.root = self.generate_root()

    def setup_treeobjects(self):
        self.adjust_GeneralContainer()
        self.adjust_sub_containers()
        self.adjust_Data()

    @staticmethod
    def generate_root():
        subnodes = {}
        root_elements = session.query(GeneralContainer).all()
        for root_element in root_elements:
            subnodes[root_element.__caption__] = Node(root_element.__caption__, root_element.__subnodes__)
        leafs = {}
        root = Node('/', subnodes, leafs)
        return root

    @staticmethod
    def adjust_GeneralContainer():
        @property
        def __subnodes__(self):
            return {"SOC": Node("SOC", self.dict_of_specific_other_containers),
                    "SC": Node("SC", self.dict_of_specific_containers)}

        @property
        def __leafs__(self):
            return {}

        GeneralContainer.__subnodes__ = __subnodes__
        GeneralContainer.__leafs__ = __leafs__

    @staticmethod
    def adjust_sub_containers():
        @property
        def __subnodes__(self):
            return self.dict_of_data

        @property
        def __leafs__(self):
            return {}

        SpecificContainer.__subnodes__ = __subnodes__
        # SpecificOtherContainer.__subnodes__ = __subnodes__
        SpecificContainer.__leafs__ = __leafs__
        # SpecificOtherContainer.__leafs__ = __leafs__


    @staticmethod
    def adjust_Data():
        @property
        def __content__(self):
            return self.content

        @__content__.setter
        def __content__(self, content):
            self.__content__ = content

        Data.__content__ = __content__


############
# OFM-classs
############

class OFM(object):
    """
    Implement as Singleton?
    """
    def __init__(self, nodeable):
        self.root = nodeable

    @staticmethod
    def getFromDict(dataDict, mapList):
        logging.debug("OFM.getFromDict, dataDict: %s, mapList: %s" %(dataDict, mapList))
        try:
            return reduce(lambda d, k: d.__subnodes__[k], mapList, dataDict)
        except KeyError, e:
            print ("KeyError: %s" % e)
            return None

    @staticmethod
    def setInDict(dataDict, mapList, value):
        OFM.getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value

    @staticmethod
    def is_node(db_object):
        o = db_object
        return hasattr(o, '__caption__') & hasattr(o, "__subnodes__") & hasattr(o, '__leafs__')

    @staticmethod
    def is_leaf(db_object):
        o = db_object
        return hasattr(o, '__caption__') & hasattr(o, "__content__")

    def path2object(self, path):
        logging.info("OFM.path2object, path: %s" % path)
        if path == '/':
            logging.debug("OFM.path2object, switch '/'")
            db_object = self.root
        else:
            logging.debug("OFM.path2object, switch 'else'")
            mapList = path.split('/')[1:] # the starting '/' leads to an empty first list entry
            db_object = self.getFromDict(self.root, mapList)
        return db_object

    ##############
    # Fuse-methods
    ##############
    def getattr(self, path):
        logging.info("OFM.getattr, path: %s" % path)
        db_object = self.path2object(path)
        if self.is_node(db_object):
            mode = stat.S_IFDIR | 0755
            st = Stat(st_mode=mode, st_size=Stat.DIRSIZE, st_nlink=2)
        elif self.is_leaf(db_object):
            logging.debug("OFM.getattr: db_object %s" % db_object)
            mode = stat.S_IFREG | 0644
            size = len(db_object.__content__)
            st = Stat(st_mode=mode, st_size=size)
        else:
            logging.debug("OFM.get_stats: No such file or directory")
            return -errno.ENOENT
        return st


    def readdir(self, path, offset, dh=None):
        logging.info("OFM.readdir, path: %s, offset: %s, dh: %s)" % (path, offset, dh))
        db_object = self.path2object(path)
        # logging.debug("OFM.readdir, isinstance(db_object, Node): %s" % isinstance(db_object, Node))
        # logging.debug("OFM.readdir, isinstance(db_object, Leaf): %s" % isinstance(db_object, Leaf))

        # subdirectories
        subdirectories = []
        subdirectories.append(fuse.Direntry("."))
        subdirectories.append(fuse.Direntry(".."))

        for subnode in db_object.__subnodes__.keys():
            # logging.debug("OFM.readdir, subdirectories.append(%s)" %subnode)
            subdirectories.append(fuse.Direntry(str(subnode))) # Type(caption): string, not unicode

        # vfiles
        vfiles = []
        for leaf in db_object.__leafs__:
            # logging.debug("OFM.readdir, vfiles.append(%s)" %leaf.caption)
            vfiles.append(str(leaf.__caption__))

        logging.debug("OFM.readdir, return: %r" % (subdirectories + vfiles))
        return subdirectories + vfiles

    def access(self, path, flags):
        logging.info("OFM.access, path: %s, flags: %s)" % (path, flags))
        db_object = self.path2object(path)
        if hasattr(db_object, '__caption__'):
            if hasattr(db_object, '__subnodes__') & hasattr(db_object, '__leafs__'):
                logging.debug("OFM.access: is directory!")
                return 0
            elif hasattr(db_object, '__caption__') & hasattr(db_object, '__content__'):
                logging.debug("OFM.access: is file!")
                return 0
        else:
            logging.debug("OFM.access: neither directory nor file!")
            return -errno.EACCES

    def read(self, path, size, offset, fh=None):
        logging.info("OFM.read, path: %s, size: %s, offset: %s, fh: %s)" % (path, size, offset, fh))
        data = "Kleiner Test, das ist ja wunderbar!"
        result = data[offset:offset+size]
        return result

ot = ObjectTree()
ofm = OFM(ot.root)

for key in ofm.root.__subnodes__.iterkeys():
    print key


###############
# Fuse-Specific
###############

class Stat(fuse.Stat):
    DIRSIZE = 4096

    def __init__(self, st_mode, st_size, st_nlink=1, st_uid=None, st_gid=None,
                 dt_atime=None, dt_mtime=None, dt_ctime=None):
        self.st_mode = st_mode
        self.st_ino = 0         # Ignored, but required
        self.st_dev = 0         # Ignored, but required

        self.st_nlink = st_nlink
        if st_uid is None:
            st_uid = os.getuid()
        self.st_uid = st_uid
        if st_gid is None:
            st_gid = os.getgid()
        self.st_gid = st_gid
        self.st_size = st_size
        now = datetime.datetime.utcnow()
        self.dt_atime = dt_atime or now
        self.dt_mtime = dt_mtime or now
        self.dt_ctime = dt_ctime or now

    def _get_dt_atime(self):
        return self.epoch_datetime(self.st_atime)
    def _set_dt_atime(self, value):
        self.st_atime = self.datetime_epoch(value)
    dt_atime = property(_get_dt_atime, _set_dt_atime)

    def _get_dt_mtime(self):
        return self.epoch_datetime(self.st_mtime)
    def _set_dt_mtime(self, value):
        self.st_mtime = self.datetime_epoch(value)
    dt_mtime = property(_get_dt_mtime, _set_dt_mtime)

    def _get_dt_ctime(self):
        return self.epoch_datetime(self.st_ctime)
    def _set_dt_ctime(self, value):
        self.st_ctime = self.datetime_epoch(value)
    dt_ctime = property(_get_dt_ctime, _set_dt_ctime)

    @staticmethod
    def datetime_epoch(dt):
        return calendar.timegm(dt.timetuple())

    @staticmethod
    def epoch_datetime(seconds):
        return datetime.datetime.utcfromtimestamp(seconds)


def get_caption(path):
    return os.path.basename(path)


def get_depth(path):
    """
    Return the depth of a given path, zero-based from root ('/')
    """
    if path == '/':
        return 0
    else:
        return path.count('/')


def is_metadata_file(path):
    caption = get_caption(path)
    if caption.lower() in METADATA_FILENAMES:
        return True
    else:
        return False


def is_directory(path):
    logging.debug("is_directory, (path, depth): (%s, %s)" %(path, get_depth(path)))
    if get_depth(path) == 0:
        logging.debug("is_directory, in: == 0")
        return True
    elif is_metadata_file(path):
        logging.debug("is_directory, in: is_metadata_file")
        return False
    elif get_depth(path) >= 3:
        logging.debug("is_directoryi, in: >= 3")
        return False
    elif get_depth(path) == 2:
        logging.debug("is_directory, in: == 2")
        dir_object = session.query(SpecificContainer).filter_by(caption=get_caption(path)).all()
        if len(dir_object) > 0:
            return True
    elif get_depth(path) == 1:
        logging.debug("is_directory, in: == 1")
        dir_object = session.query(GeneralContainer).filter_by(caption=get_caption(path)).all()
        if len(dir_object) > 0:
            return True
    else:
        logging.debug("is_directory, in: else")
        return False


def is_file(path):
    """
    Double check - don't use `!= is_directory`.
    """
    if is_metadata_file(path):
        return True
    elif get_depth(path) >= 3:
        return True
    else:
        return False


def get_subdirectories(path):
    logging.info("get_subdirectories, path: %s" % path)
    path_depth = get_depth(path)

    subdirectories = []
    subdirectories.append(fuse.Direntry("."))
    subdirectories.append(fuse.Direntry(".."))

    if path_depth == 0:
        generalcontainers = session.query(GeneralContainer).all()
        for generalcontainer in generalcontainers:
            subdirectories.append(fuse.Direntry(str(generalcontainer.caption))) # Type(caption): string, not unicode

    if path_depth == 1:
        generalcontainer = path2db_object(path)
        for specific_container in generalcontainer.specific_containers:
            subdirectories.append(fuse.Direntry(str(specific_container.caption))) # Type(caption): string, not unicode
    return subdirectories


def get_vfiles(path):
    logging.info("get_vfiles, path: %s" % path)
    path_depth = get_depth(path)
    vfiles = []
    if path_depth == 2:
        specific_container = path2db_object(path)
        logging.debug("get_vfiles, (specific_container, datas): (%s, %s)" %(
            specific_container.caption, specific_container.datas))
        for data in specific_container.datas:
            logging.debug("get_vfiles, data: %s" %(data.caption))
            vfiles.append(fuse.Direntry(str(data.caption))) #TYPE: str!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # for filename in METADATA_FILENAMES:
        #     vfiles.append(fuse.Direntry(filename))
    logging.debug("get_vfiles, return: %s" % vfiles)
    return vfiles


def path2db_object(path):
    logging.info("path2object: %s" % path)
    path_depth = get_depth(path)
    caption = os.path.basename(path)
    logging.debug("path2object: path=%s, caption=%s" %(path, caption))

    if path_depth == 0:
        logging.debug("path2object, in: == 0")
        return None
    elif is_directory(path):
        if path_depth == 1:
            logging.debug("path2object, in: is_directory & == 1")
            db_object = session.query(GeneralContainer).filter_by(caption=caption).one()
            return db_object
        elif path_depth == 2:
            logging.debug("path2object, in: is_directory & == 2")
            db_object = session.query(SpecificContainer).filter_by(caption=caption).one()
            return db_object
    elif caption in METADATA_FILENAMES:
        pass
    elif is_file(path):
        pass
    logging.debug("path2object, returned object: %s" % db_object)
    return db_object


def get_stats(path):
    logging.info("get_stats: %s" % path)
    if is_directory(path):
        logging.debug("get_stats: is_directory == True")
        mode = stat.S_IFDIR | 0755
        st = Stat(st_mode=mode, st_size=Stat.DIRSIZE, st_nlink=2)
    elif is_file(path):
        logging.debug("get_stats: is_file == True")
        mode = stat.S_IFREG | 0644
        st = Stat(st_mode=mode, st_size=24)
    else:
        logging.debug("get_stats: No such file or directory")
        return -errno.ENOENT
    return st


def create_object(path):
    logging.info("create_object: %s" %(path))
    path_depth = get_depth(path)
    caption = get_caption(path)
    parent_path = os.path.dirname(path)

    if path_depth == 1:
        logging.debug("create_object, path_deph == 0")
        generalcontainer = GeneralContainer(caption=caption)
        try:
            session.add(generalcontainer)
            session.commit()
        except sa.exc.IntegrityError, e:
            print e
            session.rollback()
            print "session rolled back!"
        return 0
    elif path_depth == 2:
        logging.debug("create_object, path_deph == 1")
        specificcontainer = SpecificContainer(caption=caption)
        try:
            parent_object = path2db_object(parent_path)
            parent_object.specific_containers.append(specificcontainer)
            session.commit()
        except sa.exc.IntegrityError, e:
            print e
            session.rollback()
            print "session rolled back!"
        return 0
    else:
        logging.debug("create_object, else")
        return -errno.EOPNOTSUPP