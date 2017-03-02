#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.path.dirname(__file__))

from celery import Celery

from settings import REDIS_URI
from server import setup_app

app = Celery(
    'telemock',
    broker=REDIS_URI,
    backend=REDIS_URI,
    include=['tasks']
)

flask_app = setup_app()
