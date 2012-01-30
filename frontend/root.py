
import web
from HomeProcessor import *
from superbowl import *

urls = (
  '/', 'epIndex',
  '/superbowl', 'epSuperbowl',
  '/superbowl/', 'epSuperbowl',
  '/api/home', 'epApiHome',
  '/api/home?', 'epApiHome',
  #'/api/superbowl', 'apiSuperbowl',
  '/api/superbowl?', 'epApiSuperbowl'
)

app = web.application(urls, globals())
class epIndex (object):
	def GET(self):
		f = file('static/index.htm', 'r')
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
		p = HomeProcessor(web.input('token').token)
		s = p.getProcessed()
		return s

class epApiSuperbowl(object):
    def GET(self):
		p = Superbowl(web.input('token').token)
		s = p.getProcessed()
		return s



if __name__ == "__main__":
    app.run()
