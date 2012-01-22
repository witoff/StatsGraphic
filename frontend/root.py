
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
	f = file('view/index.htm', 'r')
	s = f.read()
	f.close()
	return s
        #return "Hello, world!"
class api(object):
    def GET(self):
		p = Processor(web.input('token').token)
		return p.getProcessed()



if __name__ == "__main__":
    app.run()
