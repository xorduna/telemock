install:
	pip install -r requirements.txt

run:
	python telemock/server.py

celery:
	celery --app=telemock.celery_app:tasks_app worker -l info

celery-events:
	celery --app=telemock.celery_app:tasks_app events
