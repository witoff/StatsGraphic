import urllib2
import json
from pprint import pprint
from datetime import datetime, timedelta
from helper import *
import sys


class Grabber(object):

	def __init__(self, token):
		self.token = token
		self.uid = None
		self.getUsername()

	def __getUrl(self, endpoint, getstring=''):
		api_url = 'https://graph.facebook.com/%s?access_token=%s&' + getstring
		
		return api_url % (endpoint, self.token)

	def getUsername(self):
		if not self.uid:
			self.uid = self.__getFbObj('me')['username']
		return self.uid
		
	""" enter endpoint and getstring (which will be converted to proper api url) OR a url"""
	def __getFbObj(self, endpoint='', getstring='', url=None):
		if not url:
			url = self.__getUrl(endpoint,  getstring)
		#print url
		obj = urllib2.urlopen(url).read() 
		return json.loads(obj)

	def __filter_dates(self, arr, fromTime=getFromTime()):
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


	def __getAllExtended(self, endpoint, chunksize=25, fromTime=getFromTime()):
		print 'getting /' + endpoint
		home_all = []
		
		home_raw = self.__getFbObj(self.uid + '/' + endpoint, 'limit=' + str(chunksize))
		home = home_raw['data']
		n_requests = 1
		while True:
			filtered = self.__filter_dates(home, fromTime)
			home_all.extend(filtered)
			
			if len(filtered)!=len(home) or len(home)==0:
				break
			print '...'
			home_raw = self.__getFbObj(url=home_raw['paging']['next'])
			home = home_raw['data']
			n_requests = n_requests + 1
		
		print str(n_requests) + ' requests were made totalling ' + str(len(home_all)) + ' items'
		start = getTime(home_all[1]['updated_time'])
		stop = getTime(home_all[-1]['updated_time'])
		delta = start-stop

		print 'oldest request was at: ' + str(start) + ' to: ' + str(stop)
		print str(delta)
		
		return home_all
	
	def getFriends(self):
		user = self.__getFbObj(self.uid)
		#pprint(user)
		
		friends = self.__getFbObj(self.uid + '/friends')['data']
		pprint(friends)
		
		statuses = self.__getFbObj(self.uid + '/statuses')['data']
		pprint(friends)

		#get user info for each friend
		for f in friends:
			user = self.__getFbObj(str(f['id']))
			f['user'] = user


		#get events for each friend
		for f in friends:
			events = self.__getFbObj(f['id']+'/events')['data']
			print f['name'] + ' has %i events' % len(events)
			f['events'] = events

		return friends

	def getCheckins(self):
		print 'getting /checkins'
		checkins = self.__getFbObj(self.uid + '/checkins')
		return checkins['data']

	def getHome(self):
		return self.__getAllExtended('home', 100)
	def getFeed(self):
		return self.__getAllExtended('feed', 50, fromTime=datetime.now() - timedelta(days=365))
	

def main():
	
	print 'Running Grabber as main, automating retrieval'
	token = '<default token here>'
	if len(sys.argv)==2:
		token = sys.argv[1]

	g = Grabber(token)
	uid = g.getUsername()
	checkins = g.getCheckins()
	home = g.getHome()
	feed = g.getFeed()
	pprint(feed)

	def dump(fname, obj):
		f = file('data/%s.json' % fname, 'w')
		f.write(json.dumps(obj))
	dump('checkins', checkins)
	dump('feed', feed)
	dump('home', home)

if __name__ == "__main__":
	main()
