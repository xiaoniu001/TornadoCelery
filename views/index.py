from tornado.web import RequestHandler, asynchronous, authenticated

import json

from tornado import gen, websocket
from DataCelery.alarmData import recent_alarm_detail_data
from DataCelery.userData import check_user
from DataCelery.alarmData import IndexData, GasCloudData


class BaseHandler(RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("login_user")


class IndexHandler(BaseHandler, IndexData):
	"""
	燃气报警首页
	"""
	
	@gen.coroutine
	def get(self, *args, **kwargs):
		
		device_data = yield self.device_status_count()
		
		alarm_data = yield self.device_month_alarm_count()
		
		useful_data = yield self.device_month_useful_count()
		
		alarm_solution = yield self.device_alarm_solution()
		
		brand_alarm = yield self.device_brand_count()
		
		map_data = yield self.device_area_data()
		
		self.render("index.html", device_count=device_data, map_data=json.dumps(map_data),
		            alarm_data=alarm_data, useful_data=useful_data, alarm_solution=alarm_solution,
		            brand_alarm=json.dumps(brand_alarm), project_code="WBCLOUD", function_code="01")


class LoginHandler(BaseHandler):
	
	@asynchronous
	def get(self):
		self.render("login.html")
	
	@asynchronous
	def post(self):
		project_code = self.get_argument("project_code", "")
		function_code = self.get_argument("function_code", "")
		username = self.get_argument("username", "")
		pwd = self.get_argument("password", "")
		dwno = self.get_argument("dwno", "")
		print("登录表单接收数据", project_code, function_code, username, pwd, dwno)
		user = check_user(project_code, function_code, username, pwd, dwno)
		if user:
			self.set_secure_cookie("login_user", user["name"])
			self.set_secure_cookie("dwcode", user["areacode"] + "-" + user["dwid"])
			
			self.write(json.dumps({"success": True, "message": "登录成功！"}))
		else:
			self.write(json.dumps({"success": False, "message": "账号密码错误！"}))
		self.finish()


class AlarmHandler(BaseHandler, GasCloudData):
	
	@authenticated
	@asynchronous
	@gen.coroutine
	def get(self):
		"""
		所有报警单位的报警数据
		:return:
		"""
		unit_code = self.get_secure_cookie("dwcode")
		username = self.get_secure_cookie("login_user")
		print("aaaaaaaaaaaa")
		map_data = yield self.unit_alarm_data(unit_code.decode())
		all_alarm_data = yield self.unit_alarm_detail_data(unit_code.decode(), '')
		device_status = yield self.device_status_azdw(unit_code.decode(), '')
		print("ccccccccccccc")
		self.render("trend.html", map_data=json.dumps(map_data["area_data"]),
		            area_alarm_data=json.dumps(map_data["area_alarm_data"]),
		            all_alarm_data=json.dumps(all_alarm_data["area_alarm_data"], default=str),
		            azdwno=unit_code, device_status=json.dumps(device_status), username=username)


class AlarmDataHandler(BaseHandler, GasCloudData):
	
	@authenticated
	@asynchronous
	@gen.coroutine
	def get(self):
		"""
		该单位下的所有报警数据
		:return:
		"""
		azdwno = self.get_argument("azdwno", "")
		dwno = self.get_argument("dwno", "")
		result = yield self.unit_alarm_detail_data(azdwno, dwno)
		result["device_status"] = yield self.device_status_azdw(azdwno, dwno)
		self.write(json.dumps(result, default=str))
		self.finish()


class RecentAlarmHandler(websocket.WebSocketHandler):
	"""
	最近一小时实时数据websocket连接
	"""
	def check_origin(self, origin):
		return True
	
	def open(self, *args, **kwargs):
		
		self.write_message(dict(result=True, message="websocket服务端打开连接！"))
	
	def on_close(self):
		print("websocket服务端关闭连接")
	
	def on_message(self, message):
		req = json.loads(message)
		print(req)
		if req['req'] == "connectReq":
			data = recent_alarm_detail_data(req["azdwno"])
			print("websocket ", data)
			self.write_message(json.dumps(data, default=str))

