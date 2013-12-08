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


#Delete Topic method
@route('/topics/<topicId>', method='DELETE')
def deleteTopic(topicId):
	try:
            #print 'in try'
	    topics.remove({'_id':ObjectId(topicId)})
	except:
               abort(500, 'Error: database error')
	body = {"topicId": 'Removed Successfully'}
	return bottle.HTTPResponse(status=200, body=json.dumps(body), headers=head) 


#Add comments to topic
#POST method sample , add check to see if that topic_id exists
@route('/topics/<topicId>/comments', method='POST')
def addComments(topicId=None):

    if topicId is None:
        abort(400, "Bad Request: missing argument")
    else:
	topic = db['topics'].find({"_id": ObjectId(str(topicId))})
	if topic.count() < 1:
		abort(400, "Failed: %s not found" %(topicId))

    if request.body.read():
           data = json.loads(request.body.read())
       	   if data:
                   #print "in if data"
                   author = data['author']
                   author_comment = data['comment']
		   try:
		       result = db['topics'].update({"_id":ObjectId(str(topicId))},{"$push":{"comments":{"author":author,"comment":author_comment}}},upsert=False)   
                   except:
                          #print "\nin exception"     
                          abort(500, 'Error: database error')
                   return bottle.HTTPResponse(status=200, body=json.dumps(result), headers=head)
           else:
                abort(400, 'Error: no data in body')
    else:
         abort(400, 'Error: no body in the request')


#Get list of topics
@route('/topics', method='GET')
def get_topic():
    """
	This method is the API used for getting all topics on the reddit server.
	The route is '/topics' and the HTTP method used is GET. The data is attached 
    in the HTTP Request body as JSON. If the topics exists in storage, the list
    of topics are returned to the client.
    """
    try:
        all_topic = []
	topics = db['topics'].find()
	for topic in topics:
		all_topic.append(topic)
	print len(all_topic)
#        for each_topic in db['topics'].find():
#            topic = {}
#            topic["topicName"]=each_topic.items()[0][0]
#            topic["author"]=each_topic.items()[0][1]['author']
#            topic["topicId"]=str(each_topic.items()[1][1])
#            all_topic.append(topic)
        #print all_topic
    except:
        abort(500, 'Error: database error')
    return bottle.HTTPResponse(status=200, body=json.dumps(str(all_topic)), headers=head)


#Get topic by ID
@route('/topics/<topicId>', method='GET')
def get_topic_by_id(topicId=None):

	if topicId is None:
		abort(400, "Bad request: missing argument")
	else:

		try:
			topic = db['topics'].find_one({"_id": ObjectId(str(topicId))})

			try:
				return bottle.HTTPResponse(status=200, body=json.dumps(str(topic)), headers=head)
			except:
				abort(400, "Failed: %s not found" %(topicId))

		except Exception as e:
			print e
			abort(500, "Error: database error")


#Start server
run(host='localhost', port=8080, debug=True)
