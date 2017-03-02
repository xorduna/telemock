#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery.utils.log import get_task_logger
from celery_app import app
from celery_app import flask_app

import urllib.request
import random

from utils import create_message_response, create_callback_query_response
from models import User, Bot, Chat

logger = get_task_logger(__name__)

@app.task(name='tasks.random_replay')
def random_replay(keyboard, chat, type='chat'):
    """
        when type=chat take create_message_response
        when type=callback_query take create_callback_query_response
    """
    # select random answer
    answer = random.choice(
        [item for sublist in keyboard for item in sublist]
    )

    with flask_app.app_context():
        bot, user = Bot.get(chat['botname']), User.get(chat['username'])
        if type == 'chat':
            response = create_message_response(user, bot, answer)
        elif type == 'callback_query':
            pass
        else:
            raise ValueError("type must be chat or callback_query")


    logger.info('random_replay[type=%s] response: %s' % (type, response))
    # send answer to the callback_url
    #urllib.request.urlopen(callback_url, data=response)
