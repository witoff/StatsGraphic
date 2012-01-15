import urllib2
import json
from pprint import pprint
from datetime import datetime, timedelta
from helper import *

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


def getCheckins(uid):
	print 'getting /checkins'
	checkins = getFbObj(uid + '/checkins')

	print 'writing /checkins'
	f = open('checkins.json','w')
	f.write(json.dumps(checkins['data']))
	f.close()
	print '...done'

def getAllHome(uid):
	print 'getting /home'
	home_all = []
	
	def filter_dates(arr):
		#if last index is after start time, then return whole array
		if len(arr)==0:
			return []
		if getTime(arr[-1]['updated_time']) > getFromTime():
			return arr
		#else splice array:
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
	
	print 'writing /home'
	f = open('home.json', 'w')
	f.write(json.dumps(home_all))
	f.close()
	print '...done'



def main():
	
	#get all data 
	uid = 'witoff'

	getCheckins(uid)
	getAllHome(uid)
	exit(0)

if __name__ == "__main__":
	main()
