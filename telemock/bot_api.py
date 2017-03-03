#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simulated Calls of the Telegram API
https://core.telegram.org/bots/api
"""

from flask import current_app as app
from flask_restful import Resource, reqparse, abort
from werkzeug.datastructures import FileStorage

from random import randint
import json

from tasks import random_replay
from utils import create_empty_response
from models import Chat


class BasePostMixin():
    def post(self):
        chat = Chat.get(self.args['chat_id'])
        keyboard, _type = self.parse_reply_markup()
        if keyboard:
            # bot expect response from user
            # launch celery task
            # that will reply in a random time (1, 10)
            # with a random choice
            random_replay.apply_async(
                (keyboard, chat, _type), countdown=randint(1, 10)
            )

        return create_empty_response()

class BaseApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'chat_id', type=self.chat_id_validator, required=True,
            location='form'
        )
        self.reqparse.add_argument(
            'reply_markup', type=self.reply_markup_validator,
            required=False, location='form'
        )
        super().__init__()

    def chat_id_validator(self, value):
        if Chat.exists(value):
            return value
        else:
            raise ValueError('chat_id does\'t exist')

    def reply_markup_validator(self, value):
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            raise ValueError('reply_markup should be a dict')

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

    def parse_reply_markup(self):
        """ reply_markup is additional interface options.
            A JSON-serialized object for an inline keyboard,
            custom reply keyboard, instructions to remove reply keyboard
            or to force a reply from the user. """
        if self.is_replay_keyboard():
            return self.args['reply_markup']['keyboard'], 'chat'
        if self.is_inline_keyboard():
            return self.args['reply_markup']['inline_keyboard'], 'callback_query'
        return [], ''


class SendMessage(BaseApi, BasePostMixin):
    """
        https://core.telegram.org/bots/api#sendmessage
    """
    def __init__(self):
        super().__init__()
        self.reqparse.add_argument(
            'text', type=str, required=True, location='form'
        )
        self.args = self.reqparse.parse_args()

    def post(self):
        return super().post()


class SendPhoto(BaseApi, BasePostMixin):
    """ https://core.telegram.org/bots/api#sendphoto """

    def __init__(self):
        super().__init__()
        self.reqparse.add_argument(
            'photo', type=FileStorage,
            required=True, location='files'
        )
        self.args = self.reqparse.parse_args()
        # ignore photo
        self.args.pop('photo')

    def post(self):
        return super().post()


class SendDocument(BaseApi, BasePostMixin):
    """ https://core.telegram.org/bots/api#senddocument """

    def __init__(self):
        super().__init__()
        self.reqparse.add_argument(
            'document', type=FileStorage,
            required=True, location='files'
        )
        self.reqparse.add_argument(
            'reply_markup', type=dict, required=False, location='form'
        )
        self.args = self.reqparse.parse_args()
        # ignore document
        self.args.pop('document')

    def post(self):
        return super().post()


class SendVideo(BaseApi, BasePostMixin):
    """ https://core.telegram.org/bots/api#sendvideo """

    def __init__(self):
        super().__init__()
        self.reqparse.add_argument(
            'video', type=FileStorage,
            required=True, location='files'
        )
        self.reqparse.add_argument(
            'reply_markup', type=dict, required=False, location='form'
        )
        self.args = self.reqparse.parse_args()
        # ignore video
        self.args.pop('video')

    def post(self):
        return super().post()


class SendAudio(BaseApi, BasePostMixin):
    """ https://core.telegram.org/bots/api#sendaudio """

    def __init__(self):
        super().__init__()
        self.reqparse.add_argument(
            'audio', type=FileStorage,
            required=True, location='files'
        )
        self.args = self.reqparse.parse_args()
        # ignore audio
        self.args.pop('audio')

    def post(self):
        return super().post()


class SendChatAction(BaseApi):
    """ https://core.telegram.org/bots/api#sendchataction """

    def __init__(self):
        super().__init__()
        self.reqparse.add_argument(
            'action', type=str, required=True, location='form'
        )
        self.args = self.reqparse.parse_args()

    def post(self):
        return create_empty_response()
