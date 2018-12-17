from tornado.options import define, parse_command_line, options
from application import Application
from tornado import httpserver, ioloop

import tcelery

tcelery.setup_nonblocking_producer()

define("port", help="web监听端口", default=5003)


if __name__ == '__main__':
	parse_command_line()
	
	app = Application()
	http_server = httpserver.HTTPServer(app)
	http_server.listen(options.port, "0.0.0.0")
	ioloop.IOLoop.current().start()
	
	


