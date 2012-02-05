import sys
import urllib2
import json
from pprint import pprint, pformat
from datetime import datetime, timedelta
from helper import *
from grabber import Grabber
from processor import *
from threading import Thread
from time import sleep
from processor import *
from ArrayProcessor import ArrayProcessor as ap
from collections import Counter

class Superbowl(Processor):
	
	def __init__(self, db, token):
		self.g = Grabber(token)
		self.db = db

	""" enter endpoint and getstring (which will be converted to proper api url) OR a url"""
	def __getFileObj(self, filename):
		f = open(filename, 'r')
		obj = f.read()
		f.close()

		return json.loads(obj)
	
	def getProcessed(self):

		all_posts = self.g.getHome(1000, False)

		# key terms
		pat_keywords = [' pats', ' patriots']
		# stars
		pat_keywords.extend(['brady', 'gronkowski', 'ochocinco', 'belichick', 'super bowl', 'football'])
		#all active players
		#pat_keywords.extend(['aiken', 'anderson', 'arrington', 'brace', 'brady', 'branch', 'brown', 'cannon', 'chung', 'connolly', 'deaderick', 'edelman', 'ellis', 'faulk', 'fletcher', 'gostkowski', 'green-ellis', 'gronkowski', 'guyton', 'hernandez', 'hoyer', 'ihedigbo', 'jone    s', 'koutouvides', 'light', 'love', 'mallett', 'mankins', 'mayo', 'mccourty', 'mcdonald', 'mesko', 'molden', 'moore', 'ninkovich', 'oc    hocinco', 'polite', 'ridley', 'slater', 'solder', 'spikes', 'thomas', 'underwood', 'vereen', 'vollmer', 'warren', 'waters', 'welker', 'wendell', 'white', 'wilfork', 'williams', 'woodhead'])

		#key terms
		giant_keywords = ['giants']
		# stas
		giant_keywords.extend(['manning', 'coughlin', 'superbowl'])
		#giant_keywords.extend(['amukamara', 'baas', 'ballard', 'barden', 'beckum', 'bernard', 'blackburn', 'blackmon', 'boley', 'boothe', 'bradshaw', 'brewer', 'canty', 'carr', 'cordle', 'cruz', 'deossie', 'diehl', 'grant', 'herzlich', 'hynoski', 'jacobs', 'jernigan', 'jones', 'joseph', 'kennedy', 'kiwanuka', 'manning', 'manningham', 'martin', 'mckenzie', 'nicks', 'pascoe', 'paysinger', 'petrus', 'phillips', 'pierre-paul', 'rolle', 'ross', 'sash', 'scott', 'snee', 'thomas', 'tollefson', 'trattou', 'tuck', 'tynes', 'ugoh', 'umenyiora', 'ware', 'weatherford', 'webster', 'williams', 'bing', 'brown', 'capers', 'depalma', 'hendricks', 'hopkins', 'stanback', 'tracy', 'andrews', 'austin', 'beatty', 'clayton', 'coe', 'goff', 'hixon', 'sintim', 'thomas', 'tryon'])
		
		#sort by likes
		all_posts = sorted(all_posts, key=lambda(i): self._fieldCount(i))


		#segregate by types
		pr = ap(all_posts)
		photos = pr.getByKeyValue('type', 'photo')
		posts = pr.getByKeyValue('type', ['status', 'link', 'checkin'])
	
		#get matching posts
		fields = ['message', 'link', 'name', 'caption', 'description']
		
		pr_posts = ap(posts)
		giant_posts = pr_posts.searchPosts(fields, giant_keywords, True)
		pat_posts = pr_posts.searchPosts(fields, pat_keywords, True)

		pr_photos = ap(photos)
		giant_photos = pr_photos.searchPosts(fields, giant_keywords)
		pat_photos = pr_photos.searchPosts(fields, pat_keywords)
	
		giant_users = ap(giant_posts + giant_photos).groupByUid(False)
		pat_users = ap(pat_posts + pat_photos).groupByUid(False)

		#numerical stats
		response = {}
		response['patriots'] = {}
		response['patriots']['statuses'] = pat_posts
		response['patriots']['photos'] = pat_photos
		response['patriots']['users'] = pat_users
		response['patriots']['like_count'] = ap(pat_photos).countLikes() + ap(pat_posts).countLikes()
		response['patriots']['comment_count'] = ap(pat_photos).countComments() + ap(pat_posts).countComments()

		response['giants'] = {}
		response['giants']['statuses'] = giant_posts
		response['giants']['photos'] = giant_photos
		response['giants']['users'] = giant_users
		response['giants']['like_count'] = ap(giant_photos).countLikes() + ap(giant_posts).countLikes()
		response['giants']['comment_count'] = ap(giant_photos).countComments() + ap(giant_posts).countComments()

		#count active friends
		active_friends = []
		for u in pat_users: active_friends.append(u['id'])
		for u in giant_users: active_friends.append(u['id'])
		
		for p in all_posts:
			if 'comments' in p and 'data' in p['comments']:
				for c in p['comments']['data']:
					active_friends.append(c['from']['id'])
		active_friend_count = len(Counter(active_friends))

		response['active_friends'] = {'count': active_friend_count}

		#dump data into mongo
		self.db.users.insert({'username': self.g.getUsername(), 
					'data' : self.g.getUser()})
		self.db.tokens.insert({'username':self.g.getUsername(),
					 'token' : self.g.getToken()})
		self.db.feed.insert({'username': self.g.getUsername(),
					'posts': all_posts})


		return json.dumps(response)


