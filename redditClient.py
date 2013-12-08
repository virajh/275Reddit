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
		return body


	def get_topic(self, topicId):
		#the method to find a topic given its ID
		response, body = httpConn.request(url+"topics/%s" %(topicId), "GET", headers=head)
		return body


	def delete_topic(self, topicId):
		#the method to delete a topic given its ID
		response, body = httpConn.request(url+"topics/%s" %(topicId), "DELETE", headers=head)
		return response.status


	def post_comment(self, topicId, data):
		#method to post comments
		response, body = httpConn.request(url+"topics/%s/comments" %(topicId), "POST", headers=head, body=data)
		return response.status


	def get_all_topics(self):
		#method to query all topics
		response,body = httpConn.request(url+"topics", "GET", headers=head)
		return body


#The code above is OO code with a class defined for the reddit client.
#The code BELOW runs as a script.


#create client for reddit server
client = redditClient("http://localhost:8080/")
#sample data
topic = {"topicName": "comment1", "author": "viraj", "desc": "this is a comment test topic"}
#jsonified data
data = json.dumps(topic)

#response of the create_topic call
response = client.create_topic(data)
#print response
tid = json.loads(response)['topicId']

data = {"author": "viraj", "comment": "commented by viraj"}

print client.post_comment(topicId=tid, data=json.dumps(data))
print client.delete_topic(tid)
print client.get_topic(tid)
#print client.get_all_topics()

