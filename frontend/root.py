
import web
from HomeProcessor import *
from superbowl import *

urls = (
  '/', 'index',
  '/superbowl', 'superbowl',
  '/superbowl/', 'superbowl',
  '/api/home', 'apiHome',
  '/api/home?', 'apiHome',
  #'/api/superbowl', 'apiSuperbowl',
  '/api/superbowl?', 'apiSuperbowl'
)

app = web.application(urls, globals())
class index (object):
	def GET(self):
		f = file('static/index.htm', 'r')
		s = f.read()
		f.close()
		return s

	def POST(self):
		return self.GET()

class superbowl (object):
	def GET(self):
		f = file('static/superbowl.htm', 'r')
		s = f.read()
		f.close()
		return s

	def POST(self):
		return self.GET()

class apiHome(object):
    def GET(self):
		p = HomeProcessor(web.input('token').token)
		s = p.getProcessed()
		return s

class apiSuperbowl(object):
    def GET(self):
		p = Superbowl(web.input('token').token)
		s = p.getProcessed()
		return s



if __name__ == "__main__":
    app.run()
