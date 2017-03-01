#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simulated Calls of the Telegram API
https://core.telegram.org/bots/api
"""

from flask import current_app as app
from flask_restful import Resource, reqparse, abort

from random import randint

from tasks import random_replay

class SendMessage(Resource):
    """
        https://core.telegram.org/bots/api#sendmessage
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'chat_id', type=self.chat_id_validator, required=True,
            location='json'
        )
        self.reqparse.add_argument(
            'text', type=str, required=True, location='json'
        )
        self.reqparse.add_argument(
            'reply_markup', type=dict, required=False, location='json'
        )
        self.args = self.reqparse.parse_args()
        super(SendMessage, self).__init__()

    def chat_id_validator(self, value):
        """ Check if chats:<value> exists """
        if app.redis_client.exists('chats:%s' % value):
            return value
        else:
            raise ValueError('chat_id does\'t exist')

    def is_replay_keyboard(self):
        """
            Check if reply_markup store ReplyKeyboardMarkup
            https://core.telegram.org/bots/api#replykeyboardmarkup
         """
        if self.args['reply_markup'] and\
            self.args['reply_markup'].get('keyboard'):
            return True
        return False

    def is_inline_keyboard(self):
        """
            Check if reply_markup store InlineKeyboardMarkup
            https://core.telegram.org/bots/api#inlinekeyboardmarkup
        """
        if self.args['reply_markup'] and\
            self.args['reply_markup'].get('inline_keyboard'):
            return True
        return False

    def incr_user_msg_id(self, username):
        """
            New message increments message_id
            each user has its own message id correlation
        """
        user = 'users:%s' % username
        # incr user last_message_id
        app.redis_client.hincrby(user, 'last_message_id', 1)

    def get_chat(self):
        chat = 'chats:%s' % self.args['chat_id']
        return app.redis_client.hgetall(chat)

    def get_answers_list(self):
        if self.is_replay_keyboard():
            return self.args['reply_markup']['keyboard']
        if self.is_inline_keyboard():
            return self.args['reply_markup']['inline_keyboard']
        return []

    def post(self):
        chat = self.get_chat()
        self.incr_user_msg_id(chat[b'username'].decode('utf-8'))

        answers_list = self.get_answers_list()
        if answers_list:
            # launch celery task
            # that will reply in a random time (1, 10)
            # with a random choice
            bot = 'bots:%s' % chat[b'botname'].decode('utf-8')
            callback = app.redis_client.hget(bot, 'callback').\
                decode('utf-8')

            random_replay.apply_async(
                (answers_list, self.args['chat_id'], callback),
                countdown=randint(1, 10)
            )
        
        return self.args
