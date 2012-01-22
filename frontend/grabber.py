import urllib2
import json
from pprint import pprint
from datetime import datetime, timedelta
from helper import *
import sys


def getToken():
	if len(sys.argv)==2:
		return sys.argv[1]
	#else:
	#	return 'AAACEdEose0cBAC0VPEdE9exDakElNKoZBx2cU0UvyQF3LhvKpszMpPPr30UH0HEJEw6QaJsUPZAdjpoGcFKzQqESvZCV1xdtv0AfhKHwgZDZD'

def getUrl(endpoint, getstring=''):
	token = getToken()
	api_url = 'https://graph.facebook.com/%s?access_token=%s&' + getstring
	
	return api_url % (endpoint, token)

def getUsername():
	obj = getFbObj('me')
	return obj['username']
	
""" enter endpoint and getstring (which will be converted to proper api url) OR a url"""
def getFbObj(endpoint='', getstring='', url=None):
	if not url:
		url = getUrl(endpoint,  getstring)
	#print url
	obj = urllib2.urlopen(url).read() 
	return json.loads(obj)


def getCheckins(uid):
	print 'getting /checkins'
	checkins = getFbObj(uid + '/checkins')

	print 'writing /checkins'
	f = open('data/checkins.json','w')
	f.write(json.dumps(checkins['data']))
	f.close()
	print '...done'

def filter_dates(arr, fromTime=getFromTime()):
		#if last index is after start time, then return whole array
		if len(arr)==0:
			return []
		if getTime(arr[-1]['updated_time']) > fromTime:
			return arr
		#else splice array:
		#todo: efficent sort
		for i in range(len(arr)):
			if getTime(arr[i]['updated_time']) <= fromTime:
				return arr[1:i]
		return []


def getAllExtended(uid, endpoint, chunksize=25, fromTime=getFromTime()):
	print 'getting /' + endpoint
	home_all = []
	
	home_raw = getFbObj(uid + '/' + endpoint, 'limit=' + str(chunksize))
	home = home_raw['data']
	n_requests = 1
	while True:
		filtered = filter_dates(home, fromTime)
		home_all.extend(filtered)
		
		if len(filtered)!=len(home) or len(home)==0:
			break
		print '...'
		home_raw = getFbObj(url=home_raw['paging']['next'])
		home = home_raw['data']
		n_requests = n_requests + 1
	
	print str(n_requests) + ' requests were made totalling ' + str(len(home_all)) + ' items'
	start = getTime(home_all[1]['updated_time'])
	stop = getTime(home_all[-1]['updated_time'])
	delta = start-stop

	print 'oldest request was at: ' + str(start) + ' to: ' + str(stop)
	print str(delta)
	
	print 'writing /' + endpoint
	f = open('data/' + endpoint + '.json', 'w')
	f.write(json.dumps(home_all))
	f.close()
	print '...done'

def getFriends(uid):
	user = getFbObj(uid)
	#pprint(user)
	
	friends = getFbObj(uid + '/friends')['data']
	pprint(friends)
	
	statuses = getFbObj(uid + '/statuses')['data']
	pprint(friends)

	#get user info for each friend
	for f in friends:
		user = getFbObj(str(f['id']))
		f['user'] = user


	#get events for each friend
	for f in friends:
		events = getFbObj(f['id']+'/events')['data']
		print f['name'] + ' has %i events' % len(events)
		f['events'] = events

	#serialize
	f = open('data/friendevents.json', 'w')
	f.write(json.dumps(friends))
	exit(0)


def main():
	
	#get all data 
	#uid = 'witoff'

	uid = getUsername()
	getCheckins(uid)
	getAllExtended(uid, 'home', 100)
	getAllExtended(uid, 'feed', 50, fromTime=datetime.now() - timedelta(days=365))
	#getFriends(uid)

	exit(0)

if __name__ == "__main__":
	main()
