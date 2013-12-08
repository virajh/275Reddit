#!/usr/bin/env python
from bottle import *
import json

people = { "viraj": {"age": 23, "country": "india"}, "jeff": {"age": 67, "country": "finland"}}
#GET method samples
@route('/hello', method='GET')
def hello():
    return "Hello World!"

@route('/users', method='GET')
def getUsers():
    return BaseResponse(body=json.dumps(people), status=200)

@route('/users/<name>', method='GET')
def getUser(name=None):
    if(name):
	if name in people:
		return json.dumps(people[name])
	else:
		abort(404, "%s not found" % (name))
    else:
	abort(400, "Bad Request: Missing Argument")

#DELETE method sample
@route('/users/<name>', method='DELETE')
def deleteUser(name=None):
	if(name):
		if name in people:
			people.pop(name)
			return "Success: Deleted %s" % (name)
		else:
			abort(404, "%s not found" % (name))
	else:
		abort(400, "Bad Request: Missing Argument")

#PUT method samples
@route('/users/modify/<old>', method='PUT')
def editUserInfo(old=None):
	print "InHere"
	if not old:
		abort(400, "Bad Request: Missing Argument")
	if old in people:
		body = request.body.read()
		data = json.loads(body)
		people[old] = data
		return "Success: Modified %s" % (old)
	else:
		abort(404, "%s not found" % (name))

@route('/users/<old>/<new>', method='PUT')
def editUserName(old=None, new=None):
	print "orHere"
	if not old:
		abort(400, "Bad Request: Missing Argument")
	if not new:
		abort(400, "Bad Request: Missing Argument")
	if new in people:
		abort(409, "Conflict: %s already exists" %(new))
	if old in people:
		people[new]=people[old]
		people.pop(old)
		return "Success: Modified %s to %s" % (old, new)
	else:
		abort(404, "%s not found" % (old))


#POST method sample
@route('/users/<name>', method='POST')
def addUser(name=None):
	if name:
		if name in people:
			abort(409, "Conflict: %s already exists" %(new))
		else:
			body = request.body.read()
			data = json.loads(body)
			people[name] = data
			return "Success: User %s added" % (name)
	else:
		abort(400, "Bad Request: Missing Argument")

#JSON tester method
@route('/test', method='GET')
def call():
	print request
	body = request.body.read()
	print type(body)
	data = json.loads(body)
	print type(data)
	return "Success"

run(host='localhost', port=8080, debug=True)
