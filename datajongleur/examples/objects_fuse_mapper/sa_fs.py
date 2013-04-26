#!/usr/bin/env python
import fuse

import stat
import errno
import time
import logging

from models import *
import sql_fs_mapping as sfm

LOG_FILENAME = "LOG"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,
                    format="%(module)s --> %(message)s")

fuse.fuse_python_api = (0, 2)

class TemplateFS(fuse.Fuse):
    def __init__(self, *args, **kwargs):
        logging.info("Preparing to mount file system")
        super(TemplateFS, self).__init__(*args, **kwargs)
        self.parser.add_option(mountopt="xyz",
                               help="description which shows up with templatefs.py -h")


    # Driven by OFM

    def getattr(self, path):
        logging.debug("getattr, path:  %s" % path)
        return sfm.ofm.getattr(path)

    def access(self, path, flags):
        logging.info("access: %s (flags %s)" % (path, oct(flags)))
        return sfm.ofm.access(path, flags)

    def readdir(self, path, offset, dh=None):
        logging.info("readdir: %s (offset %s, dh %s)" % (path, offset, dh))

        # for subdirectory in sfm.get_subdirectories(path):
        #     yield subdirectory
        # for vfile in sfm.get_vfiles(path):
        #     yield vfile

        for direntry in sfm.ofm.readdir(path, offset, dh):
            yield direntry

    def read(self, path, size, offset, fh=None):
        logging.info("read: %s (size %s, offset %s, fh %s)" % (path, size, offset, fh))
        return sfm.ofm.read(path, size, offset, fh)


        # TODO: specify read
        # return -errno.EOPNOTSUPP

    # NEXT:
    def write(self, path, buf, offset, fh=None):
        logging.info("write: %s (offset %s, fh %s)" % (path, offset, fh))
        logging.debug("  buf: %r" % buf)
        return -errno.EOPNOTSUPP














    def fsinit(self):
        logging.info("Nonoption arguments: " + str(self.cmdline[1]))

        # self.xyz = self.cmdline[0].xyz
        # if self.xyz != None:
        #     logging.info("xyz set to '" + self.xyz + "'")
        # else:
        #     logging.info("xyz not set")

        logging.info("Filesystem mounted")

    def fsdestroy(self):
        logging.info("Unmounting file system")

    def statfs(self):
        logging.info("statfs")
        stats = fuse.StatVfs()
        # Fill it in here. All fields take on a default value of 0.
        return stats

    def utime(self, path, times):
        atime, mtime = times
        logging.info("utime: %s (atime %s, mtime %s)" % (path, atime, mtime))
        return -errno.EOPNOTSUPP

    def utimens(self, path, atime, mtime):
        logging.info("utime: %s (atime %s:%s, mtime %s:%s)"
                     % (path,atime.tv_sec,atime.tv_nsec,mtime.tv_sec,mtime.tv_nsec))
        return -errno.EOPNOTSUPP

    def readlink(self, path):
        logging.info("readlink: %s" % path)
        return -errno.EOPNOTSUPP

    def mknod(self, path, mode, rdev):
        logging.info("mknod: %s (mode %s, rdev %s)" % (path, oct(mode), rdev))
        return -errno.EOPNOTSUPP

    def mkdir(self, path, mode):
        logging.info("mkdir: %s (mode %s)" % (path, oct(mode)))
        # return -errno.EOPNOTSUPP
        return sfm.create_object(path)

    def unlink(self, path):
        """Deletes a file."""
        logging.info("unlink: %s" % path)
        return -errno.EOPNOTSUPP

    def rmdir(self, path):
        """Deletes a directory."""
        logging.info("rmdir: %s" % path)
        return -errno.EOPNOTSUPP

    def symlink(self, target, name):
        logging.info("symlink: target %s, name: %s" % (target, name))
        return -errno.EOPNOTSUPP

    def link(self, target, name):
        logging.info("link: target %s, name: %s" % (target, name))
        return -errno.EOPNOTSUPP

    def rename(self, old, new):
        logging.info("rename: target %s, name: %s" % (old, new))
        return -errno.EOPNOTSUPP

    def chmod(self, path, mode):
        """Changes the mode of a file or directory."""
        logging.info("chmod: %s (mode %s)" % (path, oct(mode)))
        return -errno.EOPNOTSUPP

    def chown(self, path, uid, gid):
        """Changes the owner of a file or directory."""
        logging.info("chown: %s (uid %s, gid %s)" % (path, uid, gid))
        return -errno.EOPNOTSUPP

    def truncate(self, path, size):
        logging.info("truncate: %s (size %s)" % (path, size))
        return -errno.EOPNOTSUPP

    def opendir(self, path):
        logging.info("opendir: %s" % path)

        return 0

        # TODO: specify access, e.g. like:
        # if path == "/":
        #     return 0
        # elif path in ...
        #     return 0
        # else:
        #     return -errno.EACCES

    def releasedir(self, path, dh=None):
        logging.info("releasedir: %s (dh %s)" % (path, dh))

    def fsyncdir(self, path, datasync, dh=None):
        logging.info("fsyncdir: %s (datasync %s, dh %s)"
                     % (path, datasync, dh))

    def open(self, path, flags):
        logging.info("open: %s (flags %s)" % (path, oct(flags)))

        return 0

        # TODO: specify open, e.g. like:
        # ...?
        # return -errno.EOPNOTSUPP

    def create(self, path, mode, rdev):
        logging.info("create: %s (mode %s, rdev %s)" % (path,oct(mode),rdev))
        return -errno.EOPNOTSUPP

    def fgetattr(self, path, fh=None):
        logging.debug("fgetattr: %s (fh %s)" % (path, fh))
        return self.getattr(path)

    def release(self, path, flags, fh=None):
        logging.info("release: %s (flags %s, fh %s)" % (path, oct(flags), fh))

    def fsync(self, path, datasync, fh=None):
        logging.info("fsync: %s (datasync %s, fh %s)" % (path, datasync, fh))

    def flush(self, path, fh=None):
        logging.info("flush: %s (fh %s)" % (path, fh))

    def ftruncate(self, path, size, fh=None):
        logging.info("ftruncate: %s (size %s, fh %s)" % (path, size, fh))
        return -errno.EOPNOTSUPP


def main():
    # Our custom usage message
    usage = """
    TemplateFS: A demo FUSE file system.
    """ + fuse.Fuse.fusage
    server = TemplateFS(version="%prog " + fuse.__version__,
                        usage=usage, dash_s_do='setsingle')
    server.parse(errex=1)
    # multithreaded = 0 appears to be very important.
    # I've had more complex filesystems freeze up without this.
    server.multithreaded = 0
    try:
        server.main()
    except fuse.FuseError, e:
        print str(e)

if __name__ == '__main__':
    main()

logging.info("File system unmounted")
