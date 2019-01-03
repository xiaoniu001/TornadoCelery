import time

from DataCelery import DataCelery
from DataCelery.sqlobj import MysqlSelect
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

obj_db = MysqlSelect()


class IndexData(object):
	executor = ThreadPoolExecutor(4)
	
	@run_on_executor
	def device_status_count(self):
		"""
		查询所有状态设备数量
		:return:
		"""
		sql = "SELECT count(id) as count, status FROM iwb_useingstatus group by status"
		result = obj_db.select_all(sql)
		device_num = {"00": 0, "01": 0, "02": 0, "04": 0, "05": 0, "all": 0}
		for i in result:
			device_num[i["status"]] = int(i["count"]) * 1000
			device_num["all"] += int(i["count"]) * 1000
		return device_num
	
	@run_on_executor
	def device_month_alarm_count(self):
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
	
	@run_on_executor
	def device_month_useful_count(self):
		"""
		查询年度月份设备正常记录
		:return:
		"""
		sql = "select count(id) as count, date_format(bjtime, '%m') as month from iwb_useingstatus " \
		      "where status='00' group by date_format(bjtime, '%Y-%m')"
		result = obj_db.select_all(sql)
		
		data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		for i in result:
			if i["month"]:
				data[int(i["month"]) - 1] = i["count"]
		return data
	
	@run_on_executor
	def device_alarm_solution(self):
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
	
	@run_on_executor
	def device_area_data(self):
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
		
		return data
	
	@run_on_executor
	def device_brand_count(self):
		"""
		查询设备品牌报警数
		:return:
		"""
		sql = "select count(a.id) as count, a.pno, date_format(a.bjtime, '%m') as month, status, d.jcname " \
		      "from iwb_useingstatus a, idict_devicemodel m , idict_dwinfo d " \
		      "where a.pno=m.pno and m.dwno=d.dwno  group by pno, date_format(bjtime, '%Y-%m'), status"
		result = obj_db.select_all(sql)
		
		data = {}
		
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
		
		return data


class GasCloudData(object):
	"""
	燃气云数据
	"""
	executor = ThreadPoolExecutor(4)
	
	@run_on_executor
	def device_status_azdw(self, azdwno, dwno):
		"""
		查询安装单位或者该安装单位下某单位设备状态数量
		:param azdwno 安装单位编码
		:param dwno 单位编码
		:return:
		"""
		print("==============")
		if azdwno and dwno:
			sql = "SELECT count(id) as count, status FROM iwb_useingstatus where azdwno='{0}' and dwno='{1}' " \
			      "group by status".format(azdwno, dwno)
		else:
			sql = "SELECT count(id) as count, status FROM iwb_useingstatus where azdwno='{}' " \
			      "group by status".format(azdwno)
		result = obj_db.select_all(sql)
		data = []
		for i in result:
			if i['status'] == "00":
				data.append(dict(value=int(i["count"]), name="正常"))
			elif i['status'] == "01":
				data.append(dict(value=int(i["count"]), name="报警"))
			elif i['status'] == "02":
				data.append(dict(value=int(i["count"]), name="失效"))
			elif i['status'] == "04":
				data.append(dict(value=int(i["count"]), name="关机"))
			elif i['status'] == "05":
				data.append(dict(value=int(i["count"]), name="故障"))
		return data
	
	@run_on_executor
	def unit_alarm_data(self, azdwno):
		"""
		:param azdwno 安装单位编号
		安装单位下的地区报警数据
		:return:
		"""
		sql = "SELECT count(*) as count, d.azdwno, w.Addr as address, w.areacode, w.dwno, d.jingdu, " \
		      "d.weidu FROM iwb_useingstatus d, idict_dwinfo w " \
		      "where d.azdwno='{0}' and d.dwno=w.dwno group by d.dwno".format(azdwno)
		result = obj_db.select_all(sql)
		area_array = [[float(i["weidu"]), float(i["jingdu"])] for i in result]
		return dict(area_data=area_array, area_alarm_data=result)
	
	@run_on_executor
	def unit_alarm_detail_data(self, azdwno, dwno):
		"""
		:param azdwno 安装单位编号
		:param dwno 单位编号
		被安装区域下的所有报警信息数据
		:return:
		"""
		
		if azdwno and dwno:
			sql = "SELECT sb.imei, sb.deviceid, sb.jingdu, sb.weidu, sb.address, sb.principal, sb.installdate, " \
			      "sb.deviceLocation, sb.status FROM iwb_useingstatus sb where sb.azdwno='{0}' and sb.dwno='{1}'".format(
				azdwno, dwno)
		else:
			sql = "SELECT sb.imei, sb.deviceid, sb.jingdu, sb.weidu, sb.address, sb.principal, sb.installdate, " \
			      "sb.deviceLocation, sb.status FROM iwb_useingstatus sb where sb.azdwno='{0}'".format(azdwno)
		result = obj_db.select_all(sql)
		area_array = [[float(i["weidu"]), float(i["jingdu"])] for i in result]
		return dict(area_data=area_array, area_alarm_data=result)
	
	
def recent_alarm_detail_data(azdwno):
	"""
	最近所有地区报警数据
	:param azdwno 安装单位编号
	:return:
	"""
	if azdwno:
		# sql = "SELECT sb.deviceid, sb.jingdu, sb.weidu, sb.address, sb.bjtime, " \
		#       "sb.deviceLocation, sb.status FROM iwb_useingstatus sb where sb.azdwno='{0}' " \
		#       "and sb.bjtime > DATE_SUB(NOW(),INTERVAL 1 HOUR)".format(azdwno)
		sql = "SELECT sb.deviceid, sb.jingdu, sb.weidu, sb.address, sb.bjtime, " \
		      "sb.deviceLocation, sb.status FROM iwb_useingstatus sb where sb.azdwno='{0}' " \
		      "limit 10".format(azdwno)
	else:
		return dict(area_data=[], area_alarm_data=[])
	result = obj_db.select_all(sql)
	area_array = [[float(i["weidu"]), float(i["jingdu"])] for i in result]
	return dict(area_data=area_array, area_alarm_data=result)


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
	GasCloudData().recent_alarm_detail_data("320211-610001")
