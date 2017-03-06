#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime

from models import User, Chat

def env_setting(setting_name, default=''):
    """ Fetch setting value from env, if not exist take default """
    if os.environ.get(setting_name):
        return os.environ[setting_name]
    return default


def get_utc_timestamp():
    t = (datetime.utcnow()-datetime.fromtimestamp(0)).total_seconds()
    return int(t)


def create_empty_response():
    """ Send empty response if bot not expect answer from user """
    return {'ok': True, 'result': []}


def create_base_message(user, bot, text):
    """
    {
        message_id: int,
        from: { ... }
        chat: { ... }
        date: timestamp,
        text: 'message'
    }
    """

    # from which bot message will be sended
    _from = {
        'username': bot['botname'],
        'first_name': bot['botname'],
        'id': bot['id']
    }
    # to what user message will be sended
    _chat = {**user, **{'type': 'private'}}

    return {
        'chat': _chat,
        'message_id': User.incr_user_msg_id(user['username']),
        'from': _from,
        'text': text,
        'date': get_utc_timestamp()
    }


def create_message_response(user, bot, text, is_ok=True):
    """
        Generate fake telegram response in such format
        https://core.telegram.org/bots/api#message
        {
            ok: bool
            result: {
                message_id: int,
                from: { ... }
                chat: { ... }
                date: timestamp,
                text: 'message'
            }
        }
        }
    """

    return {
        'ok': is_ok,
        'result': create_base_message(user, bot, text)
    }


def create_callback_query_response(user, bot, text, data, is_ok=True):
    """
        Generate fake telegram response in such format
        https://core.telegram.org/bots/api#callbackquery
        {
            ok: bool
            result: [{
                callback_query: {
                    message: {
                        message_id: int,
                        from: { ... }
                        chat: { ... }
                        date: timestamp,
                        text: 'message'
                    },
                    from: {},
                    data: 'data'
                }
            }]
        }
    """

    return {
        'ok': is_ok,
        'result': [{
            'callback_query': {
                'message': create_base_message(user, bot, text),
                'from': user,
                'data': data
            }}
        ]
    }


def create_fake_message(user, bot, chat, text):
    """
    {
        u'message': {
            u'from': {
                u'username': u'xorduna',
                u'first_name': u'xavi',
                u'id': 15610499
            },
            u'text': u'/start',
            u'entities': [
                {u'length': 6, u'type': u'bot_command', u'offset': 0}
            ],
            u'chat': {
                u'username': u'xorduna',
                u'first_name': u'xavi',
                u'type': u'private',
                u'id': 15610499
            },
            u'date': 1488558871,
            u'message_id': 177
        },
        u'update_id': 399565371
    }

    {u'message': {u'date': 1488559366, u'text': u'wola', u'from': {u'username': u'xorduna', u'first_name': u'xavi', u'id': 15610499}, u'message_id': 178, u'chat': {u'username': u'xorduna', u'first_name': u'xavi', u'type': u'private', u'id': 15610499}}, u'update_id': 399565372}

    :param user:
    :param bot:
    :param text:
    :return:
    """

    update_id = Chat.incr_update_id(chat['id'])
    return {
        'message': {
            'from': {
                'username': user['username'],
                'first_name': user['first_name'],
                'id': user['id']
            },
            'text': text,
            #'entities': [
            #    {'length': 6, u'type': u'bot_command', u'offset': 0}
            #],
            'chat': {
                'username': user['username'],
                'first_name': user['first_name'],
                'type': u'private',
                'id': chat['id']
            },
            u'date': get_utc_timestamp(),
            u'message_id': 177
        },
        u'update_id': update_id
    }