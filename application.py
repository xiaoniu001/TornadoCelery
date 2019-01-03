from tornado import web
import os

from views import index


class Application(web.Application):
	def __init__(self):
		
		handlers = [
			(r"/", index.IndexHandler),
			(r"/login", index.LoginHandler),
			(r"/alarm", index.AlarmHandler),
			(r"/alarmData", index.AlarmDataHandler),
			(r"/recentAlarm", index.RecentAlarmHandler),
			
		]
		settings = dict(
			tornado_title="燃气云",
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			xsrf_cookies=True,
			cookie_secret="Qyis855562wlm",
			login_url="/",
			debug=True,
		)
		super(Application, self).__init__(handlers, **settings)


if __name__ == '__main__':
	print(os.path.dirname(__file__))
