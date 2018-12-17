import pymysql

import time
from log.logger import error_logger

from config import *
from DataCelery import DataCelery


@DataCelery.task
def add():
	time.sleep(10)
	
	return "定时任务"


class MysqlSelect(object):
	"""
	mysql数据库操作
	"""
	
	def __init__(self, db, port, user, pwd, host, charset):
		self.__db = db
		self.__port = port
		self.__user = user
		self.__pwd = pwd
		self.__host = host
		if charset:
			self.__charset = charset
		else:
			self.__charset = "utf8mb4"
		self.__connect = None
		self.__cursor = None
	
	def __connect_db(self):
		self.__connect = pymysql.connect(host=self.__host, user=self.__user, password=self.__pwd, db=self.__db,
		                                 port=self.__port, charset=self.__charset,
		                                 cursorclass=pymysql.cursors.DictCursor,
		                                 connect_timeout=60)
		self.__cursor = self.__connect.cursor()
	
	def __close_db(self):
		self.__connect.close()
		self.__cursor.close()
	
	def select_one(self, sql):
		"""
		查询单条数据
		:param sql: 数据库语句
		:return:
		"""
		try:
			self.__connect_db()
			self.__cursor.execute(sql)
			result = self.__cursor.fetchone()
			
			return result
		except Exception as e:
			error_logger.error("查询数据失败！{}".format(e))
		finally:
			self.__close_db()
	
	def select_all(self, sql):
		"""
		查询多条数据
		:param sql:
		:return:
		"""
		try:
			self.__connect_db()
			self.__cursor.execute(sql)
			result = self.__cursor.fetchall()
			
			return result
		except Exception as e:
			error_logger.error("查询数据失败！{}".format(e))
		finally:
			self.__close_db()


obj_db = MysqlSelect(db=mysql_db, port=mysql_port, user=mysql_user, pwd=mysql_pwd,
                     host=mysql_host, charset="utf8mb4")


def device_count():
	"""
	查询所有的设备数量
	:return:
	"""
	sql = "select count(id) as count from iwb_useingstatus"
	result = obj_db.select_one(sql)
	return result


def device_month_install_count():
	"""
	查询当月安装设备的数量
	:return:
	"""
	sql = "select count(id) as count from iwb_useingstatus where " \
	      "DATE_FORMAT(installdate,'%Y%m')=DATE_FORMAT(CURDATE(),'%Y%m')"
	result = obj_db.select_one(sql)
	return result


def device_alarm_count():
	"""
	查询所有报警设备数量
	:return:
	"""
	sql = "SELECT count(id) as count FROM iwb_useingstatus where status='01'"
	result = obj_db.select_one(sql)
	return result


@DataCelery.task
def device_status_count():
	"""
	查询所有状态设备数量
	:return:
	"""
	sql = "SELECT count(id) as count, status FROM iwb_useingstatus group by status"
	result = obj_db.select_all(sql)
	device_num = {"00": 0, "01": 0, "02": 0, "04": 0, "05": 0, "all": 0}
	for i in result:
		device_num[i["status"]] = i["count"]
		device_num["all"] += i["count"]
	return device_num


def device_alarm_month_count():
	"""
	查询当月设备报警数量
	:return:
	"""
	sql = "SELECT count(id) as count FROM iwb_useingstatus where status='01' " \
	      "and DATE_FORMAT(bjtime,'%Y%m')=DATE_FORMAT(CURDATE(),'%Y%m')"
	result = obj_db.select_one(sql)
	return result


def device_close_count():
	"""
	查询关闭设备数量
	:return:
	"""
	sql = "SELECT count(id) as count FROM iwb_useingstatus where status='04'"
	result = obj_db.select_one(sql)
	return result


def device_useless_count():
	"""
	查询失效设备数量
	:return:
	"""
	sql = "SELECT count(id) as count FROM iwb_useingstatus where status='02'"
	result = obj_db.select_one(sql)
	return result


@DataCelery.task
def device_month_alarm_count():
	"""
	查询年度月份设备报警记录
	:return:
	"""
	sql = "select count(id) as count, date_format(bjtime, '%m') as month from iwb_useingstatus " \
	      "where status='01' group by date_format(bjtime, '%Y-%m');"
	result = obj_db.select_all(sql)
	data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for i in result:
		data[int(i["month"]) - 1] = i["count"]
	return data


@DataCelery.task
def device_month_useful_count():
	"""
	查询年度月份设备正常记录
	:return:
	"""
	sql = "select count(id) as count, date_format(bjtime, '%m') as month from iwb_useingstatus " \
	      "where status='00' group by date_format(bjtime, '%Y-%m')"
	result = obj_db.select_all(sql)
	print(result)
	data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for i in result:
		if i["month"]:
			data[int(i["month"]) - 1] = i["count"]
	return data


@DataCelery.task
def device_alarm_solution():
	"""
	查询报警解除记录
	:return:
	"""
	sql = "select count(id) as count, date_format(bjjctime, '%m') as month from iwb_useingstatus " \
	      "where status='00' and bjjctime>bjtime group by date_format(bjjctime, '%Y-%m');"
	result = obj_db.select_all(sql)
	data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for i in result:
		data[int(i["month"]) - 1] = i["count"]
	return data


@DataCelery.task
def device_area_data():
	"""
	查询地区设备报警数量
	:return:
	"""
	sql = "SELECT count(s.areacode) as count, s.areacode, areaname FROM iwb_useingstatus s, " \
	      "idict_areacode a where s.areacode=a.areacode group by s.areacode"
	result = obj_db.select_all(sql)
	
	data = []
	province = {}
	city = {}
	
	print("地图数据：{}".format(result))
	for i in result:
		
		li = []
		data.append(
			dict(adcode=i["areacode"], padcode=i["areacode"][0:4] + "00", value=i["count"], name=i["areaname"]))
		if i["areacode"][0:4] + "00" in city.keys():
			city[i["areacode"][0:4] + "00"][0] += i["count"]
		else:
			li.append(i["count"])
			li.append(area_name(i["areacode"][0:4] + "00")['areaname'])
			city[i["areacode"][0:4] + "00"] = li
	
	for k in city.keys():
		li = []
		if k[0:2] + "0000" in province.keys():
			province[k[0:2] + "0000"][0] += city[k][0]
		else:
			li.append(city[k][0])
			li.append(area_name(k[0:2] + "0000")['areaname'])
			province[k[0:2] + "0000"] = li
	
	for j in province.keys():
		data.append(dict(adcode=j, padcode=100000, value=province[j][0], name=province[j][1]))
	for key in city.keys():
		data.append(dict(adcode=key, padcode=key[0:2] + "0000", value=city[key][0], name=city[key][1]))
	print(data)
	return data


@DataCelery.task
def device_brand_count():
	"""
	查询设备品牌报警数
	:return:
	"""
	sql = "select count(a.id) as count, a.pno, date_format(a.bjtime, '%m') as month, status, d.jcname " \
	      "from iwb_useingstatus a, idict_devicemodel m , idict_dwinfo d " \
	      "where a.pno=m.pno and m.dwno=d.dwno  group by pno, date_format(bjtime, '%Y-%m'), status"
	result = obj_db.select_all(sql)
	
	data = {}
	print("品牌数据：{}".format(result))
	for i in result:
		arr = [[1, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [3, 0, 0, 0, 0, 0], [4, 0, 0, 0, 0, 0], [5, 0, 0, 0, 0, 0],
		       [6, 0, 0, 0, 0, 0], [7, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 0], [9, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0],
		       [11, 0, 0, 0, 0, 0], [12, 0, 0, 0, 0, 0]]
		if i["month"]:
			if i["jcname"] in data.keys():
				if i["status"] == "00":
					data[i["jcname"]][int(i["month"]) - 1][2] = i["count"]
				elif i["status"] == "01":
					data[i["jcname"]][int(i["month"]) - 1][1] = i["count"]
				elif i["status"] == "02":
					data[i["jcname"]][int(i["month"]) - 1][3] = i["count"]
				elif i["status"] == "04":
					data[i["jcname"]][int(i["month"]) - 1][4] = i["count"]
				elif i["status"] == "05":
					data[i["jcname"]][int(i["month"]) - 1][5] = i["count"]
			else:
				if i["status"] == "00":
					arr[int(i["month"]) - 1][2] = i["count"]
				elif i["status"] == "01":
					arr[int(i["month"]) - 1][1] = i["count"]
				elif i["status"] == "02":
					arr[int(i["month"]) - 1][3] = i["count"]
				elif i["status"] == "04":
					arr[int(i["month"]) - 1][4] = i["count"]
				elif i["status"] == "05":
					arr[int(i["month"]) - 1][5] = i["count"]
				data[i["jcname"]] = arr
	print(data)
	return data


def area_name(areacode):
	"""
	查询地区名称
	:param areacode 地区编码
	:return:
	"""
	sql = "SELECT areaname from idict_areacode where areacode = '{}'".format(areacode)
	result = obj_db.select_one(sql)
	return result


if __name__ == '__main__':
	pass
