run:
	python manage.py runserver

migration:
	python manage.py makemigrations && python manage.py migrate

superuser:
	python manage.py createsuperuser

celery:
	celery -A csv_project worker -l INFO