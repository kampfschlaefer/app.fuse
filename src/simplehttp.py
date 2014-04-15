
import BaseHTTPServer

class GetAppTokenHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self, *args, **kwargs):
        print "called doGET( %s, %s )" % (args, kwargs)
        print "path is %s" % self.path
        print "command is %s" % self.command
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write('''
<html>
    <head><title>app.fuse</title></head>
<body>
    <h1>app.fuse</h1>
    <p>Forwarding the access_token to the fuse app.</p>
    <script type="text/javascript">
        //document.write(window.location.hash);
        if( window.location.hash != '' ) {
            window.location.href = 'http://localhost:8000/?' + window.location.hash.replace('#','');
        }
    </script>
</body>
</html>
''')
            return
        if self.path.startswith('/?access_token='):
            self.server.access_token = self.path.split('=')[1]
            self.send_response(200)
            self.end_headers()
            self.wfile.write('''
<html>
    <head><title>app.fuse</title></head>
<body>
    <h1>app.fuse</h1>
    <p>app.fuse successfully registered with your app.net account.</p>
</body>
</html>''')
            return

        self.send_response(500)
        return
