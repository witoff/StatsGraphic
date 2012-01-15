import urllib2
import json
from pprint import pprint
from datetime import datetime, timedelta

def getUrl(endpoint, getstring=''):
	api_url = 'https://graph.facebook.com/%s?access_token=%s&' + getstring
	token = 'AAACEdEose0cBAJD2wBH3HqwNYMObM4Wquqer3hD9u2XAstlURKEIUidWeEnj97FeZApj5Hy2vKu50xPPPKKIcwZBWQjmPtMF0kqSklYgZDZD'
	
	return api_url % (endpoint, token)

""" enter endpoint and getstring (which will be converted to proper api url) OR a url"""
def getFbObj(endpoint='', getstring='', url=None):
	if not url:
		url = getUrl(endpoint,  getstring)
	#print url
	obj = urllib2.urlopen(url).read() 
	return json.loads(obj)

def getTime(t):
	return datetime.strptime(t, '%Y-%m-%dT%H:%M:%S+0000')
def getFromTime():
	return datetime.now() - timedelta(days=7)

def doCheckins(uid):
	checkins = getFbObj(uid + '/checkins')['data']
	#pprint(checkins)
	print 'you have been to %i places your whole life!' % len(checkins)

	recent = []
	for c in checkins:
		time = getTime(c['created_time'])
		if time > getFromTime():
			recent.append(c)
		else:
			break
	print 'you have been to %i places in the last week including:' % len(recent)
	for c in recent:
		print '----' + c['place']['name']
	return checkins

def doHome(uid):
	home_all = getAllHome(uid)

	#most liked
	most_liked = []
	likes = 0

	ebows = 0
	for e in home_all:
		if 'message' in e and 'ebow' in e['message']:
			ebows +=1
			
	print str(ebows) + ' out of ' + str(len(home_all)) + ' were about tebow'

	for e in home_all:
		pprint(e)
		#some things can't be liked
		if 'likes' not in e:
			continue
		#submissions by big things your following don't matter here
		if 'category' in e['from']:
			continue
		n = e['likes']['count']
		if n<likes:
			continue
		elif n == likes:
			most_liked.append(e)
		most_liked = [e]
		likes = e['likes']['count']
	
	for e in most_liked:
		print '\nmost liked: '
		pprint(e)

def getAllHome(uid):
	home_all = []
	
	def filter_dates(arr):
		#if last index is after start time, then return whole array
		if len(arr)==0:
			return []
		if getTime(arr[-1]['updated_time']) > getFromTime():
			return arr
		#else splice array
		#TODO: efficent sort
		for i in range(len(arr)):
			if getTime(arr[i]['updated_time']) <= getFromTime():
				return arr[1:i]
		return []


	home_raw = getFbObj(uid + '/home', 'limit=10')
	home = home_raw['data']
	n_requests = 1
	while True:
		filtered = filter_dates(home)
		home_all.extend(filtered)
		
		if len(filtered)!=len(home) or len(home)==0:
			break
		#print '...requesting more updates from: ' + home_raw['paging']['next']
		#print 'looking for: ' + str(getFromTime()) + ' at: ' + home[-1]['updated_time']
		print '.',
		home_raw = getFbObj(url=home_raw['paging']['next'])
		home = home_raw['data']
		n_requests = n_requests + 1
	
	print str(n_requests) + ' requests were made totalling ' + str(len(home_all)) + ' items'
	start = getTime(home_all[1]['updated_time'])
	stop = getTime(home_all[-1]['updated_time'])
	delta = start-stop

	print 'oldest request was at: ' + str(start) + ' to: ' + str(stop)
	print str(delta)
	return home_all	


def main():
	
	#get all data 
	uid = 'witoff'

	checkins = doCheckins(uid)
	home = doHome(uid)
	exit(1)

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
	f = open('friendevents.json', 'w')
	f.write(json.dumps(friends))
	exit(0)

if __name__ == "__main__":
	main()
