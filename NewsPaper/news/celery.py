import os

from celery import Celery
from django.conf import settings

app = Celery('NewsPaper')
app.config_from_object('celeryconfig')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Paper.settings')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)