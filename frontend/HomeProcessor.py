import sys
import urllib2
import json
from pprint import pprint, pformat
from datetime import datetime, timedelta
from helper import *
from processor import *
from grabber import Grabber
from threading import Thread
from time import sleep
from ArrayProcessor import ArrayProcessor as ap

class HomeProcessor(Processor):
	
	def __init__(self, db, token):
		Processor.__init__(self, token)
		self.db = db
	
	def getProcessed(self):
		response = {}	
		def runCheckins():
			response['checkins'] = self.doCheckins()
		def runHome():
			response['home'] = self.doHome()
		def runFeed():
			response['feed'] = self.doFeed()

		tc = Thread(target=runCheckins)
		th = Thread(target=runHome)
		tf = Thread(target=runFeed)

		tc.start()
		th.start()
		tf.start()
		
		while (tc.isAlive() or th.isAlive() or tf.isAlive()):
			sleep(.5)

		return json.dumps(response)

	def doCheckins(self):
		v = {} 
		
		#checkins = self.__getFileObj('data/checkins.json')
		checkins = self.g.getCheckins()
		
		v['total_count'] = len(checkins)

		#print 'you have been to %i places your whole life!' % len(checkins)

		recent = []
		for c in checkins:
			time = getTime(c['created_time'])
			if time > getFromTime():
				recent.append(c)
			else:
				break
		#print 'you have been to %i places in the last week including:' % len(recent)
		v['week_count'] = len(recent)
		v['week_names'] = []
		for c in recent:
			#print '----' + c['place']['name']
			v['week_names'].append(c['place']['name'])
		
		
		return v
	
	def doHome(self):
		v = {} 

		#home_all = self.__getFileObj('data/home.json')
		home_all = self.g.getHome()

		#
		# TEBOWS
		#
		ebows = []
		for e in home_all:
			if 'message' in e and 'ebow' in e['message']:
				ebows.append(e)

		#print '\nTEBOWS:'
		#for e in ebows:
			#print e['from']['name'] + ', ',
		#print str(len(ebows)) + ' out of ' + str(len(home_all)) + ' were about tebow'
		
		v['tebows'] = {'tebow_count': len(ebows), 'all_count': len(home_all)}

		#
		# PRESIDENTS
		#
		pres = {'gingrich' : [], 
				'romney': [], 
				'santorum' : [], 
				'paul': [],
				'obama': [],
				'colbert': []}
		def check_all(tuple, s):
			for t in tuple:
				if t in s:
					return True
			return False

		for e in home_all:
			if 'message' not in e:
				continue
			msg = e['message'].lower()
			obj = {'message': e['message'], 'name': e['from']['name']}

			if check_all(('newt', 'gingrich'),msg):
				pres['gingrich'].append(obj)
			if check_all(('santorum',),msg):
				pres['santorum'].append(obj)
				#print e['message']
			if check_all(('ron', 'paul'),msg):
				pres['paul'].append(obj)
			if check_all(('colbert',),msg):
				pres['colbert'].append(obj)
			if check_all(('obama', 'barrack'),msg):
				pres['colbert'].append(obj)
		#for k in pres:
			#print k
			#print '#' * len(pres[k])

		v['presidents'] = pres

		#FRIENDS
		home_friends = []
		for e in home_all:
			if 'category' not in e['from']:
				home_friends.append(e)


		#
		#most liked
		#
		home_friends = sorted(home_friends, key=lambda(i): self._fieldCount(i))
		#print '\nMOST LIKED:'
		v['most_liked'] = ap(home_friends).getTopPosts(3)

		#
		# Comments 
		#
		home_friends = sorted(home_friends, key=lambda(i): self._fieldCount(i, 'comments'))
		#print '\nMOST COMMENTS:'
		v['most_comments'] = ap(home_friends).getTopPosts(3)


		#
		# RATE
		#
		begin = getTime(home_all[-1]['updated_time'])
		end = getTime(home_all[0]['updated_time'])
		duration = end - begin
		dur_seconds = duration.total_seconds()
		v['time'] = {'begin' : str(begin), 'end' : str(end), 'duration': dur_seconds}

		#
		# BY TIME OF DAY
		#
		by_hour = {}
		#preallocate
		for i in range(24):
			by_hour[i] = []

		for e in home_all:
			time = getTime(e['updated_time'])
			by_hour[time.hour].append(e)

		#print '\nUSAGE BY HOUR'
		v['time']['posts'] = []
		for i in range(24):
			#print '%i: %s' % (i, '#' * len(by_hour[i]))
			v['time']['posts'].append(len(by_hour[i]))


		
		#
		# TYPE METRICS COUNTS
		#
		
		#print '\nTYPE COUNTS'
		v['type'] = {}
		for s in ['photo', 'link', 'status', 'checkin']:
			#print s.upper()
			
			home_filtered = ap(home_friends).getByKeyValue('type', s)
			home_filtered = sorted(home_filtered, key=lambda(i): self._fieldCount(i))
			if len(home_filtered) == 0:
				#print 'No posts of type: ' + s
				continue

			#print 'total of type %s: %i' % (s, len(home_filtered))
			#print '--- %s per hour' % str(len(home_filtered)/dur_seconds*3600*24)

			#print 'top:'
			top = ap(home_filtered).getTopPosts(3)
			v['type'][s] = {'count' : len(home_filtered), 'top' : top} 
			
		#
		# BY FRIEND
		#
		home_uid = ap(home_friends).groupByUid()
		v['friend'] = {'active': [], 'liked':[], 'ratio':[]}

		#print '\nMOST ACTIVE FRIENDS'
		vf = v['friend']['active'] 

		for i in range(1,6):
			obj = {}
			obj['name'] = home_uid[-i]['posts'][0]['from']['name']
			#print obj['name']
			for s in ['photo', 'link', 'status', 'checkin']:
				obj[s+'_count'] = len(ap(home_uid[-i]['posts']).getByKeyValue('type', s))
				#print ' %s: %i,' % (s, obj[s+'_count']),
			obj['total_count'] = home_uid[-i]['count']
			#print 'total: %i' % obj['total_count']
			vf.append(obj)
		
		#print '\nMOST OVERALL LIKES BY FRIEND'
		home_uid = sorted(home_uid, key=lambda(i): i['likes'])
		for i in range(1,6):
			obj = {'name': home_uid[-i]['posts'][0]['from']['name'], 'like_count' : home_uid[-i]['likes']}
			#print '%s received %i likes' % (obj['name'], obj['like_count'])
			v['friend']['liked'].append(obj)
		
		#print '\nHIGHEST LIKE RATIO OF A FRIEND'
		def ratio(i):
			if not i['likes'] or not i['count']:
				return 0
			return i['likes']/float(i['count'])
		home_uid = sorted(home_uid, key=lambda(i): ratio(i))
		for i in range(1,6):
			hid = home_uid[-i]
			obj = {}
			obj['name'] = hid['posts'][0]['from']['name'] 
			obj['like_ratio'] = float(hid['likes'])/hid['count']
			obj['like_count'] = hid['likes']
			obj['post_count'] = hid['count']
			#print '%s had a %f with %i likes over %i posts ' % (obj['name'], obj['like_ratio'], obj['like_count'], obj['post_count'])
			v['friend']['ratio'].append(obj)

		status_length = []
		sum = 0
		for e in home_all:
			if e['type']=='status' and 'message' in e:
				status_length.append(len(e['message']))
				sum += len(e['message'])
		
		v['average_status_length'] = float(sum)/len(status_length)
		#print 'average status length: %f characters' % (float(sum)/len(status_length))
		
		return v

	def doFeed(self):
		v = {} 

		#feed_all = self.__getFileObj('data/feed.json')
		feed_all = self.g.getFeed()

		#print 'PROCESSING FEED'
		#
		#most liked
		#
		feed_all = sorted(feed_all, key=lambda(i): self._fieldCount(i))
		#print '\nMOST LIKED:'
		v['most_liked'] = ap(feed_all).getTopPosts(5)

		#
		# Comments 
		#
		feed_all = sorted(feed_all, key=lambda(i): self._fieldCount(i, 'comments'))
		#print '\nMOST COMMENTS:'
		v['most_comments'] = ap(feed_all).getTopPosts(3)

		#
		# RATE
		#
		begin = getTime(feed_all[-1]['updated_time'])
		end = getTime(feed_all[0]['updated_time'])
		duration = end - begin
		dur_seconds = duration.total_seconds()
		v['time'] = {'begin' : str(begin), 'end' : str(end), 'duration': dur_seconds}
		
		#
		# BY TIME OF DAY
		#
		by_hour = {}
		#preallocate
		for i in range(24):
			by_hour[i] = []

		for e in feed_all:
			time = getTime(e['updated_time'])
			by_hour[time.hour].append(e)

		#print '\nUSAGE BY HOUR'
		v['time']['posts'] = []
		for i in range(24):
			#print '%i: %s' % (i, '#' * len(by_hour[i]))
			v['time']['posts'].append(len(by_hour[i]))


		#
		# TYPE METRICS COUNTS
		#
		
		#print '\nTYPE COUNTS'
		v['type'] = {}
		for s in ['photo', 'link', 'status', 'checkin']:
			#print s.upper()
			
			feed_filtered = ap(feed_all).getByKeyValue('type', s)
			feed_filtered = sorted(feed_filtered, key=lambda(i): self._fieldCount(i))

			#print 'total of type %s: %i' % (s, len(feed_filtered))
			#print '--- %s per hour' % str(len(feed_filtered)/dur_seconds*3600*24)

			#print 'top:'
			top = ap(feed_filtered).getTopPosts(3)
			v['type'][s] = {'count' : len(feed_filtered), 'top' : top} 
			
		#
		# BY FRIEND
		#
		feed_uid = ap(feed_all).groupByUid()
		
		v['friend'] = {'active': [], 'liked':[], 'ratio':[]}
		
		#print '\nMOST ACTIVE FRIENDS'
		
		for i in range(1,6):
			obj = {}
			
			obj['name'] = feed_uid[-i]['posts'][0]['from']['name']
			#print obj['name'] 
			
			for s in ['photo', 'link', 'status', 'checkin']:
				obj[s+'_count'] =  len(ap(feed_uid[-i]['posts']).getByKeyValue('type', s))
				#print ' %s: %i,' % (s, obj[s+'_count']),
			
			obj['total_count'] = feed_uid[-i]['count']
			#print 'total: %i' % obj['total_count'] 
			v['friend']['active'].append(obj)
			
		
		#print '\nMOST OVERALL LIKES BY FRIEND'
		feed_uid = sorted(feed_uid, key=lambda(i): i['likes'])
		for i in range(1,6):
			v['friend']['liked'].append({'name': feed_uid[-i]['posts'][0]['from']['name'], 'like_count' : feed_uid[-i]['likes']}) 
			#print '%s received %i likes' % (feed_uid[-i]['posts'][0]['from']['name'], feed_uid[-i]['likes'])
		
		#print '\nHIGHEST LIKE RATIO OF A FRIEND'
		def ratio(i):
			if not i['likes'] or not i['count']:
				return 0
			return i['likes']/float(i['count'])
		feed_uid = sorted(feed_uid, key=lambda(i): ratio(i))
		for i in range(1,6):
			fid = feed_uid[-i]
			obj = {}
			obj['name'] = fid['posts'][0]['from']['name'] 
			obj['like_ratio'] = float(fid['likes'])/fid['count']
			obj['like_count'] = fid['likes']
			obj['post_count'] = fid['count']
			#print '%s had a %f with %i likes over %i posts ' % (obj['name'], obj['like_ratio'], obj['like_count'], obj['post_count'])
			v['friend']['ratio'].append(obj)

		status_length = []
		sum = 0
		for e in feed_all:
			if e['type']=='status' and 'message' in e:
				status_length.append(len(e['message']))
				sum += len(e['message'])
		#print 'average status length: %f characters' % (float(sum)/len(status_length))
		v['average_status_length'] = float(sum)/len(status_length)
		return v

	"""Given an array of dictionaries 'arr', if arr[k] == v then add to a return array"""
def main():

	print 'Running processor as main'
	
	token = '<default token here>'
	if len(sys.argv)==2:
		token = sys.argv[1]

	p = Processor(token)

	pubvars = {}	
	checkins = p.doCheckins(pubvars)

	home = p.doHome(pubvars)
	
	feed = p.doFeed(pubvars)

	filename = 'data/processed.json'
	print 'writing to %s...' % filename 
	f = open(filename, 'w')
	f.write(json.dumps(pubvars))
	f.close()	

	filename = 'data/processed.formatted.json'
	print 'writing formatted file'
	f = open(filename, 'w')
	f.write(pformat(pubvars))
	f.close()

if __name__ == "__main__":
	main()
