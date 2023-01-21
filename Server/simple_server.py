#!/usr/bin/python

from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep    
from urllib.parse import parse_qs
from cgi import parse_header, parse_multipart
import json
import time


PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		try:
			if 'health' in self.path:
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				return

		except Exception as e:
			print("failed to fetch header" + str(e))

		if self.path=="/":
			self.path="/Server/landing_page.html"

		try:
			#Check the file extension required and
			#set the right mime type

			#Open the static file requested and send it
			f = open(curdir + sep + self.path, "rb") 
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
			return

	def parse_POST(self):

		print(self.path)
		a = self.path.find('a=')
		print(a)

		data = self.path[a:]
		splitted = data.split(';')

		mappy = {}
		for pair in splitted:
			ss = pair.split('=')
			mappy[ss[0]] = ss[1]

		mappy['current_time'] = time.strftime("%H:%M:%S", time.localtime())

		return mappy
		
	def do_POST(self):
		postvars = self.parse_POST()
		print("postvars")
		print(postvars)

		f = open(curdir + sep + '/Server/landing_page.html', "rb") 
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		self.wfile.write(f.read())
		f.close()

		f = open(curdir + sep + '/Server/last_post.html', "w") 
		f.write(json.dumps(postvars))
		f.close()

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print('^C received, shutting down the web server')
	server.socket.close()