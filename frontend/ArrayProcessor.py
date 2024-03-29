


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
	def groupByUid(self, return_posts=True):
		if len(self.arr)==0:
			return []
		post_arr = sorted(self.arr, key=lambda(i): i['from']['id'])
		posts_uid = []
		temp = []

		def getReturnObj(posts):
			ret_dict = {}
			if not len(posts):
				return {}
			ret_dict['id'] = posts[0]['from']['id']
			ret_dict['count'] = len(posts)
			ret_dict['name'] = posts[0]['from']['name']
			
			if return_posts:
				ret_dict['posts'] = posts
			
			likes = 0
			for p in posts:
				if 'likes' in p:
					likes += p['likes']['count']
			ret_dict['likes'] = likes

			return ret_dict
			

		for f in post_arr:
			if not len(temp):
				temp.append(f)
			elif f['from']['id'] == temp[0]['from']['id']:
				temp.append(f)
			else:
				posts_uid.append(getReturnObj(temp))
				temp = [f]
		posts_uid.append(getReturnObj(temp))

		posts_uid = sorted(posts_uid, key=lambda(i): i['count'])
	
		#add a field for likes count
		return posts_uid

	def getByKeyValue(self, key, vals):
		vals = self.__wrap_in_list(vals)
		ret_arr = []
		for e in self.arr:
			if e[key] in vals:
				ret_arr.append(e)
		return ret_arr

	""" if value is not a list, return [value].  Otherwise return value"""
	def __wrap_in_list(self, vals):
		if not isinstance(vals, list):
			return [vals]
		return vals


	def searchPosts(self, fields, keywords, searchComments=False):
		fields = self.__wrap_in_list(fields)	
		keywords = self.__wrap_in_list(keywords)	
		ret = []
		for post in self.arr:
			search = ""
			for f in fields:
				if f in post:
					search +=  post[f].lower()

			if searchComments:
				if 'comments' in post and 'data' in post['comments']:
					for c in post['comments']['data']:
						search += c['message'].lower()

			for k in keywords:
				if k in search:
					ret.append(post)
					break
		return ret

	def countLikes(self):
		count = 0
		for p in self.arr:
			if 'likes' in p:
				count += p['likes']['count']
			if 'comments' in p and 'data' in p['comments']:
				for c in p['comments']['data']:
					if 'likes' in c:
						count += c['likes']
		return count


	def countComments(self):
		count = 0
		for p in self.arr:
			if 'comments' in p:
				count += p['comments']['count']
		return count

