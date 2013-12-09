#!/usr/bin/env python
from bottle import *
import bottle
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

#Connection to MongoDB
mongo = MongoClient('localhost', 27017)
#Connect to database called reddit
db = mongo['reddit']
#connect to topics collection in the reddit db
global topics
topics = db['topics']
#http header object to be used in all response objects
global head
head = {'content-type': 'application/json'}

#Create Topic method
@route('/topics', method='POST')
def createTopic():

	#This method is the API used for creating a new topic on the reddit server.
	#The route is '/topics' and the HTTP method used is POST. The data is attached
	#in the HTTP Request body as JSON. If the topic is successfully created, the
	#object_id is returned to the client which uniquely identifies the topic in
	#the MongoDB backend.

	if request.body.read():
		data = json.loads(request.body.read())
		if data:
			topic = {}
			#check for author
			if data['author']:
				topic['author'] = data['author']
			else:
				abort(400, 'Error: missing author')

			#check for desc
			if data['desc']:
				topic['desc'] = data['desc']
			else:
				abort(400, 'Error: missing desc')

			#check for topicName
			if data['topicName']:
				topic['topicName'] = data['topicName']
			else:
				abort(400, 'Error: missing topicName')

			topic_id = None
			try:
				topic_id = topics.insert(topic)
			except:
				abort(500, 'Error: database error')

			body = {"topicId": str(topic_id)}
			return bottle.HTTPResponse(status=200, body=json.dumps(body), headers=head)
		else:
			abort(400, 'Error: no data in body')
	else:
		abort(400, 'Error: no body in the request')

"""
	New Comment
"""

#Delete Topic method
@route('/topics/<topicId>', method='DELETE')
def deleteTopic(topicId):
	try:
            print 'in try'
	    topics.remove({'_id':ObjectId(topicId)})
	except:
               abort(500, 'Error: database error')
	body = {"topicId": 'Removed Successfully'}
	return bottle.HTTPResponse(status=200, body=json.dumps(body), headers=head) 

#Add comments to topic
#POST method sample , add check to see if that topic_id exists


@route('/topics/<topicId>/comments', method='POST')
def addComments(topicId=None):
    if not topicId:
        abort(400, "Bad Request: Missing Argument")
    if request.body.read():
           data = json.loads(request.body.read())
       	   if data:
                   print "in if data"
                   author = data['author']
                   author_comment = data['comment']
		   try:
		       result = topics.update({"_id":ObjectId(topicId)},{"$push":{"Comments":{"author":author,"comment":author_comment}}},upsert=FALSE)
                       print result       
                   except:
                          print "\nin exception"     
                          abort(500, 'Error: database error')
                   return bottle.HTTPResponse(status=200, body=json.dumps(result), headers=head)
           else:
                abort(400, 'Error: no data in body')
    else:
         abort(400, 'Error: no body in the request')

#Start server
run(host='localhost', port=8080, debug=True)
