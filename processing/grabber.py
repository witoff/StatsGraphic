import urllib2
import json
from pprint import pprint

def getUrl(endpoint):
	api_url = 'https://graph.facebook.com/%s?access_token=%s'
	token = 'AAACEdEose0cBAGZBlBAE0rYin9Cp94qW7F7BESYO4h5JhwF4AN8JORzq76ai9mLprG9de5eZAvvH9rqx3GrAi8WhgK3ZCgIpe3nIsrneQZDZD'
	
	return api_url % (endpoint, token)

def getUrlObj(endpoint):
	url = getUrl(endpoint)
	obj = urllib2.urlopen(url).read() 
	return json.loads(obj)

#get all friends
friends = getUrlObj('witoff/friends')['data']

#get user info for each friend
for f in friends:
	user = getUrlObj(str(f['id']))
	f['user'] = user


#get events for each friend
for f in friends:
	events = getUrlObj(f['id']+'/events')['data']
	print f['name'] + ' has %i events' % len(events)
	f['events'] = events

#serialize
f = open('friendevents.json', 'w')
f.write(json.dumps(friends))
exit(0)

