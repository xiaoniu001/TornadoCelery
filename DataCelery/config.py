from kombu import Exchange, Queue
from celery.schedules import crontab

mysql_db = "wbcloud"
mysql_port = 3306
mysql_user = "root"
mysql_pwd = "85540001"
mysql_host = "121.41.27.124"
charset = "utf8mb4"


CELERY_RESULT_BACKEND = 'amqp://guest:guest@localhost:5672'
BROKER_URL = 'amqp://guest:guest@localhost:5672'

CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'

CELERY_QUEUES = (
	Queue('default', Exchange('default'), routing_key='default'),
	Queue('schedule', Exchange('schedule'), routing_key='schedule'),
	Queue('for_task_map', Exchange('for_task_map'), routing_key='for_task_map'),
	Queue('for_task_compute', Exchange('for_task_compute'), routing_key='for_task_compute'),
)

# 定义默认的QUEUE, EXCHANGE和ROUTING_KEY
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'

# 定义任务队列
CELERY_ROUTES = (
	{
		'DataCelery.alarmData.device_area_data': {
			'queue': 'for_task_map',
			'routing_key': 'for_task_map'
		}
	},
	{
		'DataCelery.alarmData.device_brand_count': {
			'queue': 'for_task_compute',
			'routing_key': 'for_task_compute'
		}
	}
)

CELERYBEAT_SCHEDULE = {
	'map': {
		'task': 'DataCelery.alarmData.add',
		'schedule': crontab(minute="*/1"),  # 每分钟执行
		'options': dict(exchange='schedule', routing_key='schedule')
	}
}
