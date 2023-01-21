#!/usr/bin/python

from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep    
from urllib.parse import parse_qs
from cgi import parse_header, parse_multipart
import json
import time


PORT_NUMBER = 8080

last_post = None

def notify_telegram(mappy):
	from telethon.sync import TelegramClient
	api_id = mappy['apii']
	api_hash = mappy['hashh']

	from telethon import TelegramClient, events, sync

	# These example values won't work. You must get your own api_id and
	# api_hash from https://my.telegram.org, under API Development.
	client = TelegramClient('session_name', api_id, api_hash)
	client.start()

	client.send_message('me', mappy['a'])

	return

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
		a = self.path.find('a=')
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

		f = open(curdir + sep + '/Server/landing_page.html', "rb") 
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		self.wfile.write(f.read())
		f.close()

		if not last_post:
			last_post = postvars

		try:
			if last_post['a'] != postvars['a']:
				print('Status changed! was ' + last_post['a'] + ' And now: ' + postvars['a'])
				notify_telegram(postvars)

		except:
			pass

		mappy['apii'] = 'XXX'
		mappy['hashh'] = 'XXX'

		f = open(curdir + sep + '/Server/last_post.html', "w") 
		f.write(json.dumps(postvars))
		f.close()

		last_post = postvars

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