#! /usr/bin/python
from pymongo import Connection
from collections import Counter
users = [u['username'] for u in Connection().pspct.tokens.find()]
for u in Counter(users):
	print u

