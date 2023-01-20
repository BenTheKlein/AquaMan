#!/usr/bin/python

from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		try:
			if "clear.sample.txt" in self.path:
				import os
				os.remove('sample.txt')
				open('clear.sample.txt', 'a')
		except:
			pass

		file_object = open('sample.txt', 'a')

		try:
			if 'health' in self.path:
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.wfile.write('OK')
				self.end_headers()
				return

		except Exception as e:
			print("failed to fetch header" + str(e))

		file_object.close()

		if self.path=="/":
			self.path="/index_example2.html"

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