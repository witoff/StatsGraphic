


class ArrayProcessor(object):
	def __init__(self, arr):
		self.arr = arr

	def getTopPosts(self, n):
		ret = []
		if len(self.arr) < n:
			n = len(self.arr)
		for i in range(1,n+1):

			obj = {}
			obj['from'] = self.arr[-i]['from']['name']
			if 'likes' in self.arr[-i]:
				obj['like_count'] = self.arr[-i]['likes']['count']
			obj['id'] = self.arr[-i]['from']['id']
			if 'message' in self.arr[-i]:
				obj['msg'] = self.arr[-i]['message']
			if 'comments' in self.arr[-i]:
				obj['comments'] = self.arr[-i]['comments']['count']
			ret.append(obj)
			if 'picture' in self.arr[-i]:
				obj['picture'] = self.arr[-i]['picture']

		return ret

	"""Given a post self.array, return an self.array of posts sorted by the poster's ID like:
		[{'id': USER_ID,
		  'posts': [POSTS_HERE...],
		  'count' : len(posts)
		}, 
		...]
	"""
	def groupByUid(self):
		post_arr = sorted(self.arr, key=lambda(i): i['from']['id'])
		home_uid = []
		temp = []

		for f in post_arr:
			if not len(temp):
				temp.append(f)
			elif f['from']['id'] == temp[0]['from']['id']:
				temp.append(f)
			else:
				home_uid.append({'id': temp[0]['from']['id'],
					'posts': temp, 
					'count' : len(temp)})
				temp = [f]
		home_uid.append({'id': temp[0]['from']['id'], 
							'posts': temp, 
							'count' : len(temp)})
		home_uid = sorted(home_uid, key=lambda(i): i['count'])
	
		#add a field for likes count
		for u in home_uid:
			likes = 0
			for e in u['posts']:
				if 'likes' in e:
					likes += e['likes']['count']
			u['likes'] = likes

		return home_uid

	def getByKeyValue(self, k, v):
		ret_arr = []
		for e in self.arr:
			if e[k] == v:
				ret_arr.append(e)
		return ret_arr

