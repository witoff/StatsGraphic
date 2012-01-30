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

class Superbowl(Processor):
	
	def __init__(self, token):
		self.g = Grabber(token)

	""" enter endpoint and getstring (which will be converted to proper api url) OR a url"""
	def __getFileObj(self, filename):
		f = open(filename, 'r')
		obj = f.read()
		f.close()

		return json.loads(obj)
	
	def getProcessed(self):

		posts = self.g.getHome()

		pat_posts = []
		# key terms
		pat_keywords = [' pats', ' patriots', ' new england', ' ne']
		# stars
		pat_keywords.extend(['brady', 'gronkowski', 'ochocinco', ' welker', 'belichick'])
		#all active players
		#pat_keywords.extend(['aiken', 'anderson', 'arrington', 'brace', 'brady', 'branch', 'brown', 'cannon', 'chung', 'connolly', 'deaderick', 'edelman', 'ellis', 'faulk', 'fletcher', 'gostkowski', 'green-ellis', 'gronkowski', 'guyton', 'hernandez', 'hoyer', 'ihedigbo', 'jone    s', 'koutouvides', 'light', 'love', 'mallett', 'mankins', 'mayo', 'mccourty', 'mcdonald', 'mesko', 'molden', 'moore', 'ninkovich', 'oc    hocinco', 'polite', 'ridley', 'slater', 'solder', 'spikes', 'thomas', 'underwood', 'vereen', 'vollmer', 'warren', 'waters', 'welker', 'wendell', 'white', 'wilfork', 'williams', 'woodhead'])

		giant_posts = [] 
		#key terms
		giant_keywords = ['giants', 'new york', ' ny']
		# stas
		giant_keywords.extend(['coughlin', 'manning', 'bradshaw', 'diehl ', ' snee', ' baas ', ' canty', 'webster', ' rolle'])
		#giant_keywords.extend(['amukamara', 'baas', 'ballard', 'barden', 'beckum', 'bernard', 'blackburn', 'blackmon', 'boley', 'boothe', 'bradshaw', 'brewer', 'canty', 'carr', 'cordle', 'cruz', 'deossie', 'diehl', 'grant', 'herzlich', 'hynoski', 'jacobs', 'jernigan', 'jones', 'joseph', 'kennedy', 'kiwanuka', 'manning', 'manningham', 'martin', 'mckenzie', 'nicks', 'pascoe', 'paysinger', 'petrus', 'phillips', 'pierre-paul', 'rolle', 'ross', 'sash', 'scott', 'snee', 'thomas', 'tollefson', 'trattou', 'tuck', 'tynes', 'ugoh', 'umenyiora', 'ware', 'weatherford', 'webster', 'williams', 'bing', 'brown', 'capers', 'depalma', 'hendricks', 'hopkins', 'stanback', 'tracy', 'andrews', 'austin', 'beatty', 'clayton', 'coe', 'goff', 'hixon', 'sintim', 'thomas', 'tryon'])

		for p in posts:

			if 'message' in p:
				m = p['message'].lower()

				for s in pat_keywords:
					if s in m:
						pat_posts.append(p)
						break
				for s in giant_keywords:
					if s in m:
						giant_posts.append(p)
			else:
				#TODO: Look for checkins, image captions etc
				pass

		#
		pat_posts = sorted(pat_posts, key=lambda(i): self._fieldCount(i))
		giant_posts = sorted(giant_posts, key=lambda(i): self._fieldCount(i))

		response = {}
		response['pat_posts'] = pat_posts
		response['giant_posts'] = giant_posts
		return json.dumps(response)
