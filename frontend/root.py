
import web
from HomeProcessor import *
from superbowl import *
from pymongo import Connection

urls = (
  '/', 'epIndex',
  '/support', 'epSupport',
  '/superbowl', 'epSuperbowl',
  '/superbowl/', 'epSuperbowl',
  '/api/home', 'epApiHome',
  '/api/home?', 'epApiHome',
  #'/api/superbowl', 'apiSuperbowl',
  '/api/superbowl?', 'epApiSuperbowl'
)
db = Connection().pspct
app = web.application(urls, globals())
class epIndex (object):
	def GET(self):
		f = file('static/index.htm', 'r')
		s = f.read()
		f.close()
		return s

	def POST(self):
		return self.GET()
class epSupport (object):
	def GET(self):
		f = file('static/support.htm', 'r')
		s = f.read()
		f.close()
		return s

	def POST(self):
		return self.GET()


class epSuperbowl (object):
	def GET(self):
		f = file('static/superbowl.htm', 'r')
		s = f.read()
		f.close()
		return s

	def POST(self):
		return self.GET()

class epApiHome(object):
    def GET(self):
		p = HomeProcessor(db, web.input('token').token)
		s = p.getProcessed()

		return s

class epApiSuperbowl(object):
    def GET(self):
		p = Superbowl(db, web.input('token').token)
		s = p.getProcessed()
		return s



if __name__ == "__main__":
    app.run()
