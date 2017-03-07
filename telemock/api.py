#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app
from flask_restful import Resource, reqparse, abort

from urllib.parse import urlparse

from models import User, Chat, Bot

#import tasks
from celery_app import make_celery

tasks_app = make_celery()

class UserApi(Resource):

    def username_validator(self, value):
        """ Check if username is unique """
        print(dir(User))
        if User.exists(value):
            raise ValueError('username should be unique')
        else:
            return value

    def delete_user_validator(self, value):
        if User.exists(value):
            return value
        else:
            abort(400, username='username does\'t exist')

    def post(self):
        _reqparse = reqparse.RequestParser()
        _reqparse.add_argument(
            'username', type=self.username_validator, required=True,
            location='json'
        )
        _reqparse.add_argument(
            'first_name', type=str, required=True, location='json'
        )
        _reqparse.add_argument(
            'last_name', type=str, required=True, location='json'
        )
        user = User.create(**_reqparse.parse_args())
        return {'user': user}, 201

    def delete(self, username):
        self.delete_user_validator(username)
        User.delete(username)
        return {}, 204

    def get(self):
        return {'users': User.get_all()}


class BotApi(Resource):

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

    def delete_bot_validator(self, value):
        if Bot.exists(value):
            return value
        else:
            abort(400, botname='botname does\'t exist')

    def post(self):
        _reqparse = reqparse.RequestParser()
        _reqparse.add_argument(
            'botname', type=self.botname_validator, required=True,
            location='json'
        )
        _reqparse.add_argument(
            'callback', type=self.url_validator, required=True,
            location='json'
        )
        _reqparse.add_argument(
            'token', type=str, required=True, location='json'
        )
        bot = Bot.create(**_reqparse.parse_args())
        return {'bot': bot}, 201

    def delete(self, botname):
        self.delete_bot_validator(botname)
        Bot.delete(botname)
        return {}, 204

    def get(self):
        return {'bots': Bot.get_all()}


class ChatApi(Resource):

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

    def chat_id_validator(self, value):
        if Chat.exists(value):
            return value
        else:
            abort(400, chat_id='chat_id does\'t exist')

    def post(self):
        _reqparse = reqparse.RequestParser()
        _reqparse.add_argument(
            'username', type=self.username_validator, required=True, location='json'
        )
        _reqparse.add_argument(
            'botname', type=self.botname_validator, required=True,
            location='json'
        )

        chat = Chat.create(**_reqparse.parse_args())
        tasks_app.send_task('tasks.start_chat', kwargs={'chat': chat})
        #tasks.start_chat.delay(chat)
        return {'chat': chat}, 201

    def put(self, chat_id):
        """ activate/deactivate chat """
        _reqparse = reqparse.RequestParser()
        _reqparse.add_argument(
            'active', type=bool, required=True, location='json'
        )
        args = _reqparse.parse_args()

        self.chat_id_validator(chat_id)
        Chat.update(chat_id, 'active', args['active'])
        return {}, 204

    def delete(self, chat_id):
        self.chat_id_validator(chat_id)
        Chat.delete(chat_id)
        return {}, 204

    def get(self):
        return {'chats': Chat.get_all()}


class ChatMessage(Resource):
    def __init__(self):
        """ Input data validation """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'text', type=str, required=True, location='json'
        )
        self.args = self.reqparse.parse_args()
        super(ChatMessage, self).__init__()

    def chat_id_validator(self, value):
        if Chat.exists(value):
            return value
        else:
            abort(400, chat_id='chat_id does\'t exist')

    def post(self, chat_id):
        """ activate/deactivate chat """
        self.chat_id_validator(chat_id)
        #Chat.update(chat_id, 'active', self.args['active'])
        chat = Chat.get(chat_id)
        #tasks.send_message.delay(chat, self.args['text'])
        tasks_app.send_task('task.send_message', kwargs={'chat': chat, 'message': self.args['text']})
        return {}, 204
