import requests as req
import json

def sendPostMutation(url, mutation, payload):
	# url = 'http://127.0.0.1:8888/graphql/'
	try:
		r = req.post(url, json={'query': mutation, 'variables': payload})
		return json.loads(r.content)
	except req.exceptions.RequestException as e:
		raise Exception(e)