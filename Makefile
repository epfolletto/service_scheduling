run:
	poetry run python3 manage.py runserver
mmg:
	poetry run python3 manage.py makemigrations
migrate:
	poetry run python3 manage.py migrate
redis:
	docker run -d -p 6379:6379 redis
cel:
	cd appointment && poetry run celery -A tasks worker -l info --pool=solo
fl:
	cd appointment && poetry run celery -A tasks flower --address=127.0.0.1 --port=5566