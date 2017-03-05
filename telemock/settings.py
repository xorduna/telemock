#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import logging

from utils import env_setting

DEBUG = env_setting('DEBUG', True)
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'test-secret-key'

LOG_FILE = env_setting('LOG_FILE', os.path.join('/tmp/logs', 'telemock_api.log'))
LOG_LEVEL = env_setting('LOG_LEVEL', logging.INFO)
LOG_FORMAT = env_setting('LOG_FORMAT', '%(process)d [%(asctime)s] [%(levelname)s]: %(message)s ')

# used as a backend and message broker
REDIS_URI = env_setting(
    'REDIS_URI', 'redis://{host}:{port}/{db}'.format(
        host='localhost',
        port=6379,
        db=0
    )
)

BROKER_URI = env_setting('BROKER_URI', REDIS_URI)

try:
    from settings_local import *
except ImportError:
    pass
