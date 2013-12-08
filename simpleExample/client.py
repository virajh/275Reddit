#!/usr/bin/env python
import httplib2
import urllib
from json import loads, dumps

class sampleClient:

	def __init__(self, api_url):
		global url
		url = api_url
		global h
	        h = httplib2.Http(".cache")  

	def getUsers(self):
		response, body = h.request(url+"users", "GET", headers=None)
		print response
		return body

	def getUser(self, name, head):
		response, body = h.request(url+"users/%s" % (name), "GET", headers=head)
		return body

	def create(self, name, body, head):
		response, body = h.request(url+"users/%s" % (name), "POST", headers=head, body=body)
		return body

	def modifyName(self, name, newname, head):
		response, body = h.request(url+"users/%s/%s" %(name, newname), "PUT", headers=head)
		return body

	def modify(self, name, body, head):
		response, body = h.request(url+"users/modify/%s" %(name), "PUT", headers=head, body=body)
		return body

	def delete(self, name, head):
		response, body = h.request(url+"users/%s" %(name), "DELETE", headers=head)
		return body

	def greet(self, head):
		response, body = h.request(url+"hello", "GET", headers=head)
		return body

	def testJson(self, data, header):
		response, body = h.request(url+"test", "GET", headers=header, body=data)
		return body

client = sampleClient('http://localhost:8080/')
headers = {'content-type': 'application/json'}
data = {"age": "dead", "location": "unknown"}
body = dumps(data)

#print client.greet()
#print client.testJson(body, headers)
#print client.create("jack", body, headers)
#print client.create("jack", body, headers)
#print client.getUsers()
#print client.getUser('viraj', headers)
#print client.modify("viraj", body, headers)
#print client.modifyName('jack', 'Jack', headers)
#print client.delete('jack', headers)

