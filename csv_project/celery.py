import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csv_project.settings')

app = Celery('csv_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')