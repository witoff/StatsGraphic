
import web

urls = (
  '/', 'index',
  '/api', 'api',
  '/api?', 'api'
)

app = web.application(urls, globals())

class index (object):
    def GET(self):
	f = file('index.htm', 'r')
	s = f.read()
	f.close()
	return s
        #return "Hello, world!"
class api(object):
    def GET(self):
	return web.input('token').token



if __name__ == "__main__":
    app.run()
