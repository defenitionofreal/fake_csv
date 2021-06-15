web: gunicorn csv_project.wsgi
release: python manage.py migrate
worker: celery -A csv_project worker