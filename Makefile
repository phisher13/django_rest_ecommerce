run:
	python manage.py runserver 8080

migrate:
	docker-compose exec web python manage.py migrate

migrations:
	docker-compose exec web python manage.py makemigrations

super:
	docker-compose exec web python manage.py createsuperuser

req:
	docker-compose exec web pip freeze > requirements.txt

tests:
	docker-compose exec web python manage.py test ecommerce/tests

