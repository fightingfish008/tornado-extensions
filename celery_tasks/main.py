
from celery import Celery
from celery_tasks import config

celery_app = Celery('celery_tasks', broker=config.broker_url)

# 加载配置
# celery_app.config_from_object('celery_tasks.config')

# 让celery自动发现任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])
