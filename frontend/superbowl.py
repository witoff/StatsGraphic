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

class Superbowl(processor):
	
	def __init__(self, token):
		self.g = Grabber(token)

	""" enter endpoint and getstring (which will be converted to proper api url) OR a url"""
	def __getFileObj(self, filename):
		f = open(filename, 'r')
		obj = f.read()
		f.close()

		return json.loads(obj)
	
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
