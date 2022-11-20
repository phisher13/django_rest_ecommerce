run:
	python manage.py runserver 8080

migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

super:
	python manage.py createsuperuser

req:
	pip freeze > requirements.txt

tests:
	python manage.py test ecommerce/tests