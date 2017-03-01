#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery.utils.log import get_task_logger
from celery_app import app

import random

logger = get_task_logger(__name__)

@app.task(name='tasks.random_replay')
def random_replay(answers_list, chat_id, callback_url):
    # select random answer
    answer = random.choice(
        [item for sublist in answers_list for item in sublist]
    )
    logger.info('random_replay send answer: %s' % answer)
    # TODO: send answer to the callback_url
