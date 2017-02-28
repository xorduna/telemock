#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app
from flask_restful import Resource, reqparse, abort

from urllib.parse import urlparse


class User(Resource):
    def __init__(self):
        """ Input data validation """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username', type = str, required = True,
            help = 'username field is required', location = 'json'
        )
        self.reqparse.add_argument(
            'first_name', type = str, required = True,
            help = 'first_name field is required', location = 'json'
        )
        self.reqparse.add_argument(
            'second_name', type = str, required = True,
            help = 'second_name field is required', location = 'json'
        )
        self.args = self.reqparse.parse_args()
        super(User, self).__init__()

    def post(self):
        user_id = app.redis_client.incr('last_user_id', amount=1)
        self.args['active'], self.args['id'] = True, user_id
        # save user as a hash - users:user_id
        app.redis_client.hmset('users:%d' % user_id, self.args)
        return {'user': self.args}, 201


class Bot(Resource):
    def __init__(self):
        """ Input data validation """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'botname', type=self.botname_validator, required=True, location='json'
        )
        self.reqparse.add_argument(
            'callback', type=self.url_validator, required=True, location='json'
        )
        self.reqparse.add_argument(
            'token', type=str, required=True, location='json'
        )
        self.args = self.reqparse.parse_args()
        super(Bot, self).__init__()

    def url_validator(self, value):
        res = urlparse(value)
        if res.scheme and res.netloc and res.path:
            return value
        else:
            raise ValueError("callback should be a valid url")

    def botname_validator(self, value):
        """ Check if botname is unique """
        if app.redis_client.exists('bots:%s' % value):
            raise ValueError('botname should be unique')
        else:
            return value

    def post(self):
        self.args['id'] = app.redis_client.incr('last_bot_id', amount=1)
        # save bot as a hash - bots:botname
        app.redis_client.hmset('bots:%s' % self.args['botname'], self.args)
        return {'bot': self.args}, 201


class Chat(Resource):
    def __init__(self):
        """ Input data validation """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username', type=str, required=True, location='json'
        )
        self.reqparse.add_argument(
            'botname', type=self.botname_validator, required=True,
            location='json'
        )
        self.args = self.reqparse.parse_args()
        super(Chat, self).__init__()

    def botname_validator(self, value):
        """ Check if bots:<value> exists """
        if app.redis_client.exists('bots:%s' % value):
            return value
        else:
            raise ValueError('botname does\'t exist')

    def post(self):
        self.args['id'] = app.redis_client.incr('last_chat_id', amount=1)
        # save chat as a hash - chats:<chat_id>
        app.redis_client.hmset('chats:%s' % self.args['id'], self.args)
        return {'chat': self.args}, 201


class ChatById(Resource):
    def __init__(self):
        """ Input data validation """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'active', type=bool, required=True, location='json'
        )
        self.args = self.reqparse.parse_args()
        super(ChatById, self).__init__()

    def chat_id_validator(self, value):
        """ Check if chats:<value> exists """
        if app.redis_client.exists('chats:%s' % value):
            return value
        else:
            abort(400, chat_id='chat_id does\'t exist')

    def put(self, chat_id):
        """ activate/deactivate chat """
        self.chat_id_validator(chat_id)
        app.redis_client.hset('chats:%s' % chat_id,
            'active', self.args['active']
        )
        return {'chat': 'chat'}, 204
