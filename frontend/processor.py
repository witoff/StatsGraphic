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

	"""if obj[field] exists, return obj[field]['count']"""
	def _fieldCount(self, obj, field='likes'):
		if field in obj:
			return obj[field]['count']
		else:
			return 0

