from sandbox import app as application
from gevent.wsgi import WSGIServer

if __name__ == '__main__':
	#application.run(debug=False)
	http_server = WSGIServer(('', 5000), application)
	http_server.serve_forever()
