#!/usr/bin/python

from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep    
from urllib.parse import parse_qs
from cgi import parse_header, parse_multipart
import json
import time

import smtplib
from email.mime.text import MIMEText

PORT_NUMBER = 8080

last_post = None

def notify_email(mappy):
	sender_email = mappy['EMAIL_SENDER']
	sender_password = mappy['EMAIL_TOKEN']
	recipient_email = mappy['EMAIL_REC']


	subject = "AQUA NOTIFICATION IMPORTANT!!" + time.strftime("%x, %X, %y, %Y")
	body = """
		<html>
		<body>
		<p>This is an <b>HTML</b> email sent from Python using the Gmail SMTP server.</p>
		</body>
		</html>
	"""

	if mappy['a'] == '0':
		body = """
		<html>
			<body>
				<p><b>LOW WATER LEVEL!</b></p>
			</body>
		</html>
		"""

	if mappy['a'] == '1':
		body = """
		<html>
			<body>
				<p><b>BACK TO NORMAL!</b></p>
			</body>
		</html>
		"""


	html_message = MIMEText(body, 'html')
	html_message['Subject'] = subject
	html_message['From'] = sender_email
	html_message['To'] = recipient_email
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.login(sender_email, sender_password)
	server.sendmail(sender_email, recipient_email, html_message.as_string())
	server.quit()

	return


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
			print(ss[0])
			mappy[ss[0]] = ss[1]

		mappy['current_time'] = time.strftime("%x, %X, %y, %Y")

		return mappy
		
	def do_POST(self):
		global last_post

		postvars = self.parse_POST()

		try:
			f = open(curdir + sep + '/Server/landing_page.html', "rb") 
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
		except Exception as e:
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

		if not last_post:
			last_post = postvars

		try:
			print('TEMP:::::: Status changed! was ' + last_post['a'] + ' And now: ' + postvars['a'])
			if last_post['a'] != postvars['a']:
				print('Status changed! was ' + last_post['a'] + ' And now: ' + postvars['a'])
				notify_email(postvars)

		except Exception as e:
			print(e)
			pass

		postvars['EMAIL_TOKEN'] = 'XXX'

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