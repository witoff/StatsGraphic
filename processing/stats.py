import json
from pprint import pprint

#load
f = open('friendevents.json','r')
friends = json.loads(f.read())
pprint(friends[0])

#preprocess
n_events = [len(f['events']) for f in friends]

#stats
print 'OVERALL STATS'
total = sum(n_events)
average = float(total)/len(n_events)
print 'number of friends: ' + str(len(n_events))
print 'average: ' + str(average)
n_events.sort()
print 'median: ' + str(n_events[len(n_events)/2])

