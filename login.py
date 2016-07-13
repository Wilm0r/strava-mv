#!/usr/bin/python

APP = {
	"id": 12108,
	"client_secret": "1679a24c0e1d23f75bec3cecf8082f676b55d877",
}
FN = "access_token"

import BaseHTTPServer
import os
import SocketServer
import sys
import urlparse

from stravalib.client import Client

client = Client()
code = sys.argv[1:]  # Won't even try handling HTTP reqs if we already have the code.

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		url = urlparse.urlparse(self.path)
		if url.path == "/authorized":
			q = urlparse.parse_qs(url.query)
			if "code" in q:
				# Add the resulting code to global array
				# checked by the while loop below.
				code.extend(q["code"])
			self.send_response(200)
			self.end_headers()
			self.wfile.write("Thanks! Now go back to your terminal. :-)")
		else:
			self.send_error(404)

# Port doesn't matter so let the kernel pick one.
httpd = SocketServer.TCPServer(("", 0), Handler)
port = httpd.server_address[1]

authorize_url = client.authorization_url(
	client_id=APP["id"],
	redirect_uri="http://localhost:%d/authorized" % port,
	scope="write")

print "Now open the following URL and authorise this application."
print "Then Strava should send you to a localhost:%d URL handled by this script." % port
print "If that fails, rerun this script passing the code= value as an argument."
print
print authorize_url

# "code" gets updated once Strava calls us back.
while not code:
	httpd.handle_request()

access_token = client.exchange_code_for_token(
	client_id=APP["id"],
	client_secret=APP["client_secret"], code=code)

client.access_token = access_token
athlete = client.get_athlete()

print
print "Logged in as %s <%s>. Writing access token to file %s" % (athlete.firstname, athlete.email, FN)

f = file(FN, "w")
os.chmod(FN, 0600) # file won't do this as an extra argument, grrr
f.write(access_token)
