
import web
from HomeProcessor import *

urls = (
  '/', 'index',
  '/api/home', 'home',
  '/api/home?', 'home'
)

app = web.application(urls, globals())

class index (object):
	def GET(self):
		f = file('static/superbowl.htm', 'r')
		s = f.read()
		f.close()
		return s

	def POST(self):
		return self.GET()

class home(object):
    def GET(self):
		p = HomeProcessor(web.input('token').token)
		s = p.getProcessed()
		#s = s.replace('\n','')
		return s


if __name__ == "__main__":
    app.run()
