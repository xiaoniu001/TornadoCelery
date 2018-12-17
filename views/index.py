from tornado.web import RequestHandler, asynchronous
import json
import time
from DataCelery.alarmData import DataCelery
from tornado import gen
from DataCelery.alarmData import device_status_count, device_month_alarm_count, device_month_useful_count, \
	device_alarm_solution, device_brand_count, device_area_data


class IndexHandler(RequestHandler):
	"""
	燃气报警首页
	"""
	
	@gen.coroutine
	def get(self, *args, **kwargs):
		
		get_time = time.clock()
		
		MAP = DataCelery.AsyncResult("map")
		print(MAP.result)
		device_data = yield gen.Task(device_status_count.apply_async)
		
		alarm_data = yield gen.Task(device_month_alarm_count.apply_async)
		
		useful_data = yield gen.Task(device_month_useful_count.apply_async)
		
		alarm_solution = yield gen.Task(device_alarm_solution.apply_async)
		
		brand_alarm = yield gen.Task(device_brand_count.apply_async)
		map_time = time.clock()
		map_data = yield gen.Task(device_area_data.apply_async)
		print(time.clock()-get_time, time.clock()-map_time)
		self.render("index.html", device_count=device_data.result, map_data=json.dumps(map_data.result),
		            alarm_data=alarm_data.result, useful_data=useful_data.result, alarm_solution=alarm_solution.result,
		            brand_alarm=json.dumps(brand_alarm.result))
		
class NoBlockingHnadler(RequestHandler):
	
	@asynchronous
	def get(self):
		print("cccccccccc")
		self.write("Hello, world")
		self.finish()
