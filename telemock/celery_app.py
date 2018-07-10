#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.path.dirname(__file__))

from celery import Celery

from settings import REDIS_URI, BROKER_URI
from server import setup_app

tasks_app = Celery(
    'telemock',
    broker=BROKER_URI,
    #backend=REDIS_URI,
    include=['tasks']
)

flask_app = setup_app()
TaskBase = tasks_app.Task

class ContextTask(TaskBase):
    abstract = True
    def __call__(self, *args, **kwargs):
        """ add flask context to base celery task class """
        with flask_app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)

tasks_app.Task = ContextTask
