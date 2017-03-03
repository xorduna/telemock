#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app
from flask_restful import Resource, reqparse, abort

from urllib.parse import urlparse

from models import User, Chat, Bot


class UserApi(Resource):
    def __init__(self):
        """ Input data validation """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username', type=self.username_validator, required=True,
            location='json'
        )
        self.reqparse.add_argument(
            'first_name', type=str, required=True, location='json'
        )
        self.reqparse.add_argument(
            'last_name', type=str, required=True, location='json'
        )
        self.args = self.reqparse.parse_args()
        super(UserApi, self).__init__()

    def username_validator(self, value):
        """ Check if username is unique """
        print(dir(User))
        if User.exists(value):
            raise ValueError('username should be unique')
        else:
            return value

    def post(self):
        user = User.create(**self.args)
        return {'user': user}, 201


class BotApi(Resource):
    def __init__(self):
        """ Input data validation """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'botname', type=self.botname_validator, required=True,
            location='json'
        )
        self.reqparse.add_argument(
            'callback', type=self.url_validator, required=True,
            location='json'
        )
        self.reqparse.add_argument(
            'token', type=str, required=True, location='json'
        )
        self.args = self.reqparse.parse_args()
        super(BotApi, self).__init__()

    def url_validator(self, value):
        res = urlparse(value)
        if res.scheme and res.netloc and res.path:
            return value
        else:
            raise ValueError("callback should be a valid url")

    def botname_validator(self, value):
        """ Check if botname is unique """
        if Bot.exists(value):
            raise ValueError('botname should be unique')
        else:
            return value

    def post(self):
        bot = Bot.create(**self.args)
        return {'bot': bot}, 201


class ChatApi(Resource):
    def __init__(self):
        """ Input data validation """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username', type=self.username_validator, required=True, location='json'
        )
        self.reqparse.add_argument(
            'botname', type=self.botname_validator, required=True,
            location='json'
        )
        self.args = self.reqparse.parse_args()
        super(ChatApi, self).__init__()

    def botname_validator(self, value):
        if Bot.exists(value):
            return value
        else:
            raise ValueError('botname does\'t exist')

    def username_validator(self, value):
        if User.exists(value):
            return value
        else:
            raise ValueError('username does\'t exist')

    def post(self):
        chat = Chat.create(**self.args)
        return {'chat': chat}, 201


class ChatByIdApi(Resource):
    def __init__(self):
        """ Input data validation """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'active', type=bool, required=True, location='json'
        )
        self.args = self.reqparse.parse_args()
        super(ChatByIdApi, self).__init__()

    def chat_id_validator(self, value):
        if Chat.exists(value):
            return value
        else:
            abort(400, chat_id='chat_id does\'t exist')

    def put(self, chat_id):
        """ activate/deactivate chat """
        self.chat_id_validator(chat_id)
        Chat.update(chat_id, 'active', self.args['active'])
        return {}, 204
