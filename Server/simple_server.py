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
			if "sample.txt" not in self.path:
				file_object.write("\n" + str(self.headers["User-Agent"]))
				
				#if 'Android' in self.headers["User-Agent"]:
				#		pass
				#else:
				#	self.send_error(404,'File Not Found: %s' % self.path)
				#	return

				try:
					file_object.write("\n" + str(self.headers["Sec-Ch-Ua-Platform"]))
				except:
					pass

				try:
					file_object.write("\n" + str(self.headers["Referer"]))
				except:
					pass

				file_object.write('                                                                                                                                                                                                                                ')
				print("\nNew connection!!!!")
				print("User-Agent: " + self.headers["User-Agent"])
				print("Platform: " + self.headers["Sec-Ch-Ua-Platform"])
				print("Referer: " + self.headers["Referer"])
		except Exception as e:
			print("failed to fetch header" + str(e))

		file_object.close()

		if self.path=="/":
			self.path="/index_example2.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html") or self.path.endswith(".txt"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".jpeg"):
				#mimetype='image/jpeg'
				#sendReply = True
				mimetype='application/x-tgsticker'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if self.path.endswith(".mp4"):
				#mimetype='video/mp4'
				mimetype='application/x-tgsticker'
				sendReply = True
			if self.path.endswith(".tgs"):
				mimetype='application/x-tgsticker'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path, "rb") 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return


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