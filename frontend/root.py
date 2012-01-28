
import web
from processor import Processor
urls = (
  '/', 'index',
  '/api', 'api',
  '/api?', 'api'
)

app = web.application(urls, globals())

class index (object):
    def GET(self):
	f = file('static/index.htm', 'r')
	s = f.read()
	f.close()
	return s
        #return "Hello, world!"
class api(object):
    def GET(self):
		p = Processor(web.input('token').token)
		s = p.getProcessed()
		#s = s.replace('\n','')
		return s



if __name__ == "__main__":
    app.run()
