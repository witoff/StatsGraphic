#! /usr/bin/python
from pymongo import Connection
from ArrayProcessor import ArrayProcessor as ap

posts = Connection().pspct.feed.find()
posts = [p for p in posts]
len(posts)
all_posts = []
for p in posts:
 for apost in p['posts']:
  all_posts.append(apost)
print len(all_posts)
print sum([len(p['posts']) for p in posts])
len(posts)
print max([len(p['posts']) for p in posts])
print min([len(p['posts']) for p in posts])
all_processor = ap(all_posts)
all_processor.searchPosts(['message','link','name','caption','description'], 'manning')
keywords = [' pats', 'patriots', 'brady', 'gronkowski', 'belichick', 'super bowl', 'superbowl', 'football', 'giants', 'manning', 'coughlin', 'superbowl']
def s(val): return len(all_processor.searchPosts(['message', 'link', 'name', 'caption', 'description'], val, True))
for k in keywords:
 print k,
 print s([k])

#import readline
#readline.write_history_file('history.txt')
