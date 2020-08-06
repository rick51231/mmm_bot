import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "core.settings")

from core.settings import BROKER_URL

celery = Celery('workers', broker=BROKER_URL)
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
