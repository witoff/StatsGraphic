#! /usr/bin/python
from pymongo import Connection
from collections import Counter
users = [u['username'] for u in Connection().pspct.tokens.find()]
grouped = Counter(users)
for u in grouped:
	print u, grouped[u]

