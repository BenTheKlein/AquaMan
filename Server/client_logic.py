#!/usr/bin/python

print('client logic starting')

#f = open('/tmp/client_logic.log', 'a')
#f.write('hahahah')
#f.close()
import requests
import os

def post(data):
	url = 'https://aquaman.onrender.com/' + data
	myobj = {'somekey': 'somevalue'}
	print('url: ' + url)

	x = requests.post(url, json = myobj)

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

	TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
	#EMAIL_REC = os.environ.get('EMAIL_REC')	
	#EMAIL_TOKEN = os.environ.get('EMAIL_TOKEN')	
	post('a=' + state + ';TELEGRAM_TOKEN=' + TELEGRAM_TOKEN + ';current_time=' + time.strftime("%x, %X, %y, %Y").replace(' ', ''))
	time.sleep(10)
	

print('client logic finished')