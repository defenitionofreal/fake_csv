web: gunicorn csv_project.wsgi --log-file -
release: python manage.py migrate
worker: celery -A csv_project worker