import sys
import urllib2
import json
from pprint import pprint, pformat
from datetime import datetime, timedelta
from helper import *
from grabber import Grabber
from threading import Thread
from time import sleep

class Processor(object):
	
	def __init__(self, token):
		self.g = Grabber(token)

	""" open the json in 'filename' """
	def __getFileObj(self, filename):
		f = open(filename, 'r')
		obj = f.read()
		f.close()

		return json.loads(obj)
	def __getTopPosts(self, arr, n):
		ret = []
		if len(arr) < n:
			n = len(arr)
		for i in range(1,n+1):

			obj = {}
			obj['from'] = arr[-i]['from']['name']
			if 'likes' in arr[-i]:
				obj['like_count'] = arr[-i]['likes']['count']
			obj['id'] = arr[-i]['from']['id']
			if 'message' in arr[-i]:
				obj['msg'] = arr[-i]['message']
			if 'comments' in arr[-i]:
				obj['comments'] = arr[-i]['comments']['count']
			ret.append(obj)
			if 'picture' in arr[-i]:
				obj['picture'] = arr[-i]['picture']

		return ret

	"""Given a post array, return an array of posts sorted by the poster's ID like:
		[{'id': USER_ID,
		  'posts': [POSTS_HERE...],
		  'count' : len(posts)
		}, 
		...]
	"""
	def __groupByUid(self, post_arr):
		post_arr = sorted(post_arr, key=lambda(i): i['from']['id'])
		home_uid = []
		arr = []

		for f in post_arr:
			if not len(arr):
				arr.append(f)
			elif f['from']['id'] == arr[0]['from']['id']:
				arr.append(f)
			else:
				home_uid.append({'posts': arr, 'count' : len(arr)})
				arr = [f]
		home_uid.append({'id': arr[0]['from']['id'], 
							'posts': arr, 
							'count' : len(arr)})
		home_uid = sorted(home_uid, key=lambda(i): i['count'])
		
		for u in home_uid:
			likes = 0
			for e in u['posts']:
				if 'likes' in e:
					likes += e['likes']['count']
			u['likes'] = likes

		return home_uid

	def __getByKeyValue(self, arr, k, v):
		ret_arr = []
		for e in arr:
			if e[k] == v:
				ret_arr.append(e)
		return ret_arr

	"""if obj[field] exists, return obj[field]['count']"""
	def __fieldCount(self, obj, field='likes'):
		if field in obj:
			return obj[field]['count']
		else:
			return 0

