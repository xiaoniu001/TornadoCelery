import pymysql
# from log.logger import error_logger
from DataCelery.config import mysql_port, mysql_pwd, mysql_host, mysql_db, mysql_user, charset


class MysqlSelect(object):
	"""
	mysql数据库操作
	"""
	
	def __init__(self):
		self.__connect = None
		self.__cursor = None
	
	def __connect_db(self):
		
		self.__connect = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_pwd, db=mysql_db,
		                                 port=mysql_port, charset=charset,
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
			# error_logger.error("查询数据失败！{}".format(e))
			print(e)
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
			# error_logger.error("查询数据失败！{}".format(e))
			print(e)
		finally:
			self.__close_db()
