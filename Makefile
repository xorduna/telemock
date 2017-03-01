install:
	pip install -r requirements.txt

run:
	python telemock/server.py

celery:
	celery --app=telemock.celery_app:app worker -l info

celery-events:
	celery --app=telemock.celery_app:app events
