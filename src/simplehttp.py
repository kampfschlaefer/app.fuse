
import BaseHTTPServer

class GetAppTokenHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self, *args, **kwargs):
        print "called doGET( %s, %s )" % (args, kwargs)
        print "path is %s" % self.path
        print "command is %s" % self.command
