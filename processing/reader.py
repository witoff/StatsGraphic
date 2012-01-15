import urllib2
import json
from pprint import pprint
from datetime import datetime, timedelta
from helper import *

""" enter endpoint and getstring (which will be converted to proper api url) OR a url"""
def getFileObj(filename):
	f = open(filename, 'r')
	obj = f.read()
	f.close()

	return json.loads(obj)

def doCheckins():
	checkins = getFileObj('checkins.json')
	
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

def showTop(arr, n):
	for i in range(1,n+1):
		print '\n%i by: %s' % (i, arr[-i]['from']['name']), 
		print ' likes: ' + str(arr[-i]['likes']['count']), 
		print ' id: ' + str(arr[-i]['id']) 
		print ' msg: ' + arr[-i]['message']

def doHome():
	home_all = getFileObj('home.json')

	#
	#tebows
	#
	ebows = []
	for e in home_all:
		if 'message' in e and 'ebow' in e['message']:
			ebows.append(e)

	print '\nTEBOWS:'
	for e in ebows:
		print e['from']['name'] + ', ',
	print str(len(ebows)) + ' out of ' + str(len(home_all)) + ' were about tebow'

	home_friends = []
	for e in home_all:
		if 'category' not in e['from']:
			home_friends.append(e)
	#
	#most liked
	#
	home_likes = []
	for e in home_friends:
		if 'likes' in e:
			home_likes.append(e)
	print len(home_likes)
	home_likes = sorted(home_likes, key=lambda(i): i['likes']['count'])
	print '\nMOST LIKED:'
	showTop(home_likes, 3)

	#
	# Comments 
	#
	home_comments = []
	for e in home_friends:
		if 'comments' in e:
			home_comments.append(e)
	home_comments = sorted(home_comments, key=lambda(i): i['comments']['count'])
	print '\nMOST COMMENTS:'
	showTop(home_comments, 3)

	#
	# PHOTO
	#
	home_photos = getByKeyValue(home_friends, 'type', 'photo')
	home_photos = sorted(home_photos, key=lambda(i): count(i))
	print '\nBEST PHOTOs:'
	showTop(home_photos, 3)	
	
	#
	# RATE
	#
	begin = getTime(home_all[-1]['updated_time'])
	end = getTime(home_all[0]['updated_time'])
	duration = end - begin
	dur_seconds = duration.total_seconds()
	
	#
	# TYPE COUNTS
	#
	print '\n TYPE COUNTS'
	for s in ['photo', 'link', 'status', 'checkin']:
		type_count = getByKeyValue(home_friends, 'type', s)
		print 'type %s: %i' % (s, len(type_count))
		print '--- %s per hour' % str(len(type_count)/dur_seconds*3600*24)

	#
	# BY FRIEND
	#
	home_friends = sorted(home_friends, key=lambda(i): i['from']['id'])
	home_uid = []
	arr = []

	for f in home_friends:
		if not len(arr):
			arr.append(f)
		elif f['from']['id'] == arr[0]['from']['id']:
			arr.append(f)
		else:
			home_uid.append({'posts': arr, 'count' : len(arr)})
			arr = [f]
	home_uid.append({'posts': arr, 'count' : len(arr)})
	home_uid = sorted(home_uid, key=lambda(i): i['count'])

	print '\nMOST ACTIVE FRIENDS'
	for i in range(1,10):
		print home_uid[-i]['posts'][0]['from']['name']
		for s in ['photo', 'link', 'status', 'checkin']:
			print ' %s: %i,' % (s, len(getByKeyValue(home_uid[-i]['posts'], 'type', s))),
		print 'total: %i' % home_uid[-i]['count']
	
	
	print '\nBy Friends:'

	

	#
	# BY TIME OF DAY
	#

	

def getByKeyValue(arr, k, v):
	ret_arr = []
	for e in arr:
		if e[k] == v:
			ret_arr.append(e)
	return ret_arr

def count(obj):
	if 'likes' in obj:
		return obj['likes']['count']
	else:
		return 0
	

def main():
	
	checkins = doCheckins()

	home = doHome()
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
