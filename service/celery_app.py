import os
import time

import celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')

app = celery.Celery('service')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
# что бы celery ароматически искала нужные таски
app.autodiscover_tasks()


@app.task()
def debug_task():
    time.sleep(20)
    print('Hello from debug task')
