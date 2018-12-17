
from celery import Celery

DataCelery = Celery('DataCelery')
DataCelery.config_from_object('DataCelery.config')
DataCelery.conf.timezone = 'Asia/Shanghai'
