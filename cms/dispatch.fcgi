#!$HOME/env/bin/python
import sys

from paste.deploy import loadapp
from flup.server.fcgi_fork import WSGIServer

app = loadapp('config:$HOME/env/spartan/production.ini')
server = WSGIServer(app)
server.run()