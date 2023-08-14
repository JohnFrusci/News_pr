CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_TIMEZONE = 'UTC'

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'weekly-newsletter': {
        'task': 'proj_name.tasks.weekly_newsletter',
        'schedule': crontab(hour=8, minute=0, day_of_week='mon'),
    },
}
