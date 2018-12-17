from tornado import web
import os

from views import index


class Application(web.Application):
	def __init__(self):
		
		handlers = [
			(r"/", index.IndexHandler),
			(r"/test", index.NoBlockingHnadler),
		]
		settings = dict(
			tornado_title="燃气云",
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			xsrf_cookies=True,
			cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
			login_url="/login",
			debug=True,
		)
		super(Application, self).__init__(handlers, **settings)


if __name__ == '__main__':
	print(os.path.dirname(__file__))
