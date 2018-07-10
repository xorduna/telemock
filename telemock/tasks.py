#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery.utils.log import get_task_logger
from celery_app import make_celery
#from celery_app import flask_app

tasks_app = make_celery()

import urllib.request
import random
import json
import requests

from utils import create_message_response, create_callback_query_response, create_fake_message
from models import User, Bot, Chat

logger = get_task_logger(__name__)

@tasks_app.task(name='tasks.random_replay')
def random_replay(keyboard, chat, type='chat'):
    """
        when type=chat take create_message_response
        when type=callback_query take create_callback_query_response
    """
    # select random answer
    print(keyboard[0])
    #options = keyboard
    answer = random.choice(keyboard[0])
    if 'text' in answer:
        answer = answer['text']

    bot = Bot.get(chat['botname'])
    user = User.get(chat['username'])

    if type == 'chat':
        response = create_fake_message(user, bot, chat, answer)
    elif type == 'callback_query':
        text, data = answer['text'], answer['callback_data']
        response = create_callback_query_response(user, bot, text, data)
    else:
        raise ValueError("type must be chat or callback_query")

    logger.info('random_replay[type=%s] response: %s' % (type, response))
    # send random answer to the callback_url
    print(response)
    r = requests.post(bot['callback'], json=response)
    print(r.text)


@tasks_app.task(name="tasks.start_chat")
def start_chat(chat):
    bot, user = Bot.get(chat['botname']), User.get(chat['username'])
    print(bot)
    #response = create_message_response(user, bot, "/start")
    response = create_fake_message(user, bot, chat, "/start")

    logger.info('send START message to bot response: %s' % (response))
    print(response)
    r = requests.post(bot['callback'], json=response)
    print(r.text)
    #   urllib.request.urlopen(bot['callback'], data=json.dumps(response))


@tasks_app.task(name="task.send_message")
def send_message(chat, message):
    bot, user = Bot.get(chat['botname']), User.get(chat['username'])
    response = create_fake_message(user, bot, chat, message)
    logger.info('send message to bot response: %s' % (response))
    print(response)
    r = requests.post(bot['callback'], json=response)
    print(r.text)
