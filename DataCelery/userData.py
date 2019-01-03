from DataCelery.sqlobj import MysqlSelect

obj_db = MysqlSelect()


def check_user(projectcode, functioncode, username, pwd, dwno):
	"""
	验证用户名密码
	:param projectcode: 项目代码
	:param functioncode: 功能代码
	:param username: 用户名
	:param pwd: 密码
	:param dwno: 单位编码
	:return:
	"""
	sql = "SELECT areacode, name, dwid FROM iwb_users where projectcode='{0}' and functioncode='{1}' and loginname='{2}' " \
	      "and pwd='{3}' and dwid='{4}'".format(projectcode, functioncode, username, pwd, dwno)
	result = obj_db.select_all(sql)
	
	if result and len(result) == 1:
		return result[0]
	else:
		print("账号密码错误或查询到多条用户！")
		pass


if __name__ == '__main__':
	check_user("320211", "420001", "administrator", "85541")
