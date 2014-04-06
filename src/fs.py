# -*- coding: utf8 -*-
#
import stat
import os
import time
import ConfigParser
import subprocess
import fuse
fuse.fuse_python_api = (0, 2)
import adnpy

import simplehttp

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

        self.config = ConfigParser.SafeConfigParser()
        self.config.add_section('Local')
        self.config.set('Local', 'cachedir', '.app.fuse.cache')
        self.config.read(['.app.fuse.conf'])

        server_address = ('', 8000)
        httpd = simplehttp.BaseHTTPServer.HTTPServer(server_address, simplehttp.GetAppTokenHandler)

        #adnpy.api.add_authorization_token(self.config.get('Auth', 'access_token'))
        subprocess.check_call([
            'xdg-open',
            'https://account.app.net/oauth/authenticate?client_id=gTTvLAtQhg4f3cqbYfAU6awFxHUuVvnb&response_type=token&redirect_uri=http://localhost:8000&scope=files'
        ])

        httpd.handle_request()

        raise Exception

        self.cachedir = self.config.get('Local', 'cachedir')

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
            #print "Append apn-files %s" % self.files.keys()
            dirents.extend(self.files.keys())
        print "dirents = %s" % dirents
        for f in dirents:
            yield fuse.Direntry(str(f))

    def _get_cache_filename(self, sha1):
        return os.path.join(
            self.cachedir,
            os.path.join(*[ sha1[i:i+4] for i in range(0, len(sha1), 4) ])
        )

    def open(self, path, flags):
        print "open(%s, %s)" % (path, flags)
        pe = path.split('/')[-1]
        if pe not in self.files.keys():
            print "%s is not a file I know" % pe
            return 0
        sha = self.files[pe]['sha1']
        #print "Looking for file with sha1 of %s" % sha
        cached_filepath = self._get_cache_filename(sha)
        if not os.path.isfile(cached_filepath):
            print "Gotta fetch that file first: %s" % cached_filepath
            #print self.files[pe]
            #print self.files[pe].keys()
            if not os.path.isdir(os.path.dirname(cached_filepath)):
                os.makedirs(os.path.dirname(cached_filepath))
            f = adnpy.api.get_file_content(self.files[pe]['id'])
            open(cached_filepath, 'w').write(f.content)

        return 0

    def read(self, path, size, offset):
        pe = path.split('/')[-1]
        cached_file = self._get_cache_filename(self.files[pe]['sha1'])
        f = open(cached_file, 'r')
        f.seek(offset)
        return f.read(size)

if __name__ == '__main__':
    fs = AppNetFs()
    fs.flags = 0
    #fs.multithreaded = 0
    fs.parse(errex=1)
    fs.main()
