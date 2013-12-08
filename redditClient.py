#!/usr/bin/env python
import httplib2
import json


class redditClient:

	def __init__(self, api_url):
		#URL of the bottle server
		global url
		url = api_url

		#http connection object, to be used by all methods
		global httpConn
	        httpConn = httplib2.Http(".cache")
		
		#http header to be used by all methods		
		global head
		head = {'content-type': 'application/json'}


	def create_topic(self, data):
		#the method to create topics
		response, body = httpConn.request(url+"topics", "POST", headers=head, body=data)
		return json.loads(body)


#The code above is OO code with a class defined for the reddit client.
#The code BELOW runs as a script.


#create client for reddit server
client = redditClient("http://localhost:8080/")

#sample data
topic = {"topicName": "sample", "author": "viraj", "desc": "this is a test topic"}
#jsonified data
data = json.dumps(topic)

#response of the create_topic call
response = client.create_topic(data)
print response['topicId']
