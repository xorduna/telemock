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
from utils import create_empty_response
from models import Chat

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
        if Chat.exists(value):
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

    def get_msg_info(self):
        """ https://core.telegram.org/bots/api#message """
        if self.is_replay_keyboard():
            return self.args['reply_markup']['keyboard'], 'chat'
        if self.is_inline_keyboard():
            return self.args['reply_markup']['inline_keyboard'], 'callback_query'
        return [], ''

    def post(self):
        chat = Chat.get(self.args['chat_id'])
        keyboard, _type = self.get_msg_info()
        if keyboard:
            # bot expect response from user
            # launch celery task
            # that will reply in a random time (1, 10)
            # with a random choice
            random_replay.apply_async(
                (keyboard, chat, _type), countdown=randint(1, 10)
            )
        
        return create_empty_response()
