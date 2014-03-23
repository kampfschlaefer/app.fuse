# -*- coding: utf8 -*-
#
import stat
import os
import time
import ConfigParser
import fuse
fuse.fuse_python_api = (0, 2)
import adnpy


class MyStat(fuse.Stat):
      def __init__(self):
          self.st_mode = stat.S_IFDIR | 0755
          self.st_ino = 0
          self.st_dev = 0
          self.st_nlink = 2
          self.st_uid = os.geteuid()
          self.st_gid = os.getegid()
          self.st_size = 4096
          self.st_atime = 0
          self.st_mtime = 0
          self.st_ctime = 0


class AppNetFs(fuse.Fuse):

    def __init__(self, *args, **kwargs):
        print "initializing app.net-fs"
        super(AppNetFs, self).__init__(*args, **kwargs)

        self.config = ConfigParser.ConfigParser()
        self.config.read(['.app.fuse.conf'])

        adnpy.api.add_authorization_token(self.config.get('Auth', 'access_token'))

        self.files = {}
        self.adn_files = adnpy.api.get_my_files()[0]
        #print self.adn_files
        for f in self.adn_files:
            self.files[f['name']] = f
        #print self.files
        print self.files.keys()

    def getattr(self, path):
        st = MyStat()
        pe = path.split('/')[-1]
        if pe in self.files:
            st.st_mode = stat.S_IFREG | 0640
            st.st_nlink = 1
            st.st_size = self.files[pe]['size']
            st.st_ctime = time.mktime(time.strptime(self.files[pe]['created_at'], '%Y-%m-%dT%H:%M:%SZ'))
            st.st_atime = st.st_ctime
            st.st_mtime = st.st_ctime
        return st

    def readdir(self, path, offset):
        print "readdir( %s, %s )" % (path, offset)
        dirents = [u'.', u'..']
        if path == '/':
            print "Append apn-files %s" % self.files.keys()
            dirents.extend(self.files.keys())
        print "dirents = %s" % dirents
        for f in dirents:
            yield fuse.Direntry(str(f))

    def read(self, path, size, offset):
        print "read(%s, %i, %i)" % (path, size, offset)
        pe = path.split('/')[-1]
        if pe not in self.files.keys():
            print "%s is not a file I know" % pe
            return 0
        return bytes(self.files[pe]['url'])[offset:size+offset]

if __name__ == '__main__':
    fs = AppNetFs()
    fs.flags = 0
    #fs.multithreaded = 0
    fs.parse(errex=1)
    fs.main()
