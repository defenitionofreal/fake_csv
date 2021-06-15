web: gunicorn csv_project.wsgi --log-file -
release: python manage.py migrate
celery: celery worker -A csv_project -l info -c 4