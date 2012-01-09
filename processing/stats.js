print('running stats...');
eval(read('jlinq/jlinq.js'));
friends = eval(read('friendevents.json'));

function ps(total, count, name)
{
	print(name + ': ' + count + ' %: ' + 100.*count/total);
}

function ave(obj)
{
 return jLinq.from(obj).average('events.length')
}
//
// BEGIN PROCESSING
//
n_friends = friends.length
print('friend count: ' + n_friends)
print('friend count: ' + jLinq.from(friends).count())

//Gender
print('\nGender')
males = jLinq.from(friends).starts('user.gender','m').select()
ps(n_friends, males.length, 'male friends')
females = jLinq.from(friends).starts('user.gender','f').select()
ps(n_friends, females.length, 'female friends')

print('\naverage friend event count: ' + ave(friends))
print('average male event count: ' + ave(males))
print('average female event count: ' + ave(females))

//Relationship
print('\nRelationship Stats:');
single = jLinq.from(friends).starts('user.relationship_status', 's').select()
inrel = jLinq.from(friends).starts('user.relationship_status', 'in').select()
eng = jLinq.from(friends).starts('user.relationship_status', 'e').select()
mar = jLinq.from(friends).starts('user.relationship_status', 'm').select()

n_rels = single.length + inrel.length + eng.length + mar.length
ps(n_rels, single.length, 'single');
ps(n_rels, inrel.length, 'in a relationship');
ps(n_rels, eng.length, 'engaged');
ps(n_rels, mar.length, 'married');

print('average single events: ' + ave(single))
print('average relati events: ' + ave(inrel))
print('average engage events: ' + ave(eng))
print('average marrie events: ' + ave(mar))

//age
seventies = jLinq.from(friends).contains('user.birthday', '/197').select()
eighties = jLinq.from(friends).contains('user.birthday', '/198').select()
nineties = jLinq.from(friends).contains('user.birthday', '/199').select()
thous = jLinq.from(friends).contains('user.birthday', '/200').select()

n_age = seventies.length + eighties.length + nineties.length + thous.length

print('\nAge stats')
ps(n_age, seventies.length, '70s');
ps(n_age, eighties.length, '80s');
ps(n_age, nineties.length, '90s');
ps(n_age, thous.length, '00s');

print('average 70 events: ' + ave(seventies))
print('average 80 events: ' + ave(eighties))
print('average 90 events: ' + ave(nineties))
print('average 00 events: ' + ave(thous))

//Event Info
print('\nEvents');
events = jLinq.from(friends).select(function(rec){return rec['events']});
var allEvents = [];
for (i in events){  
	for(j in events[i]){
		allEvents.push(events[i][j]);
	}
}

print('Total Events: ' + allEvents.length);
ids = jLinq.from(allEvents).distinct('id');
print('Unique Events: ' + ids.length);

//Events in the next 3 days

//Events coming up this weekend
