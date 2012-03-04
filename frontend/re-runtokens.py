from pymongo import Connection
import urllib

db = Connection().pspct.tokens
tokens = []
for p in db.find():
    if p['username'] not in ['witoff','kgreenek']:
            tokens.append(p['token'])

for t in tokens: 
    urllib.urlretrieve('http://pspct.com/api/superbowl?token=' + t)


