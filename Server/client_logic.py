#!/usr/bin/python

print('client logic starting')

#f = open('/tmp/client_logic.log', 'a')
#f.write('hahahah')
#f.close()
import requests

def post(data):
	URL = 'https://aquaman.onrender.com/' + data
	myobj = {'somekey': 'somevalue'}

	x = requests.post(url, json = myobj)

	print(x.text)

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
state = ''
for i in range(6):
	input_state = GPIO.input(21)
	if input_state:
		print('Full :)')
		state='1'
	else:
		print('Empty :( :( ')
		state='0'
	post('a=' + state)
	time.sleep(10)
	

print('client logic finished')