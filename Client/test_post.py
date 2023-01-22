import requests

url = 'localhost:8080'
myobj = {'somekey': 'somevalue'}

x = requests.post(url, json = myobj)

print(x.text)