#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Simple redis-py wrapper """

from flask import current_app as app

class User:
    """ User fields: 
            username, first_name, last_name, id (incremental by user),
            active (boolean), last_message_id
    """
    @staticmethod
    def get(username):
        user = 'users:%s' % username
        return app.redis_client.hgetall(user)

    @staticmethod
    def exists(username):
        """ Check if users:<username> exists """
        return app.redis_client.exists('users:%s' % username)

    @staticmethod
    def incr_user_msg_id(username):
        """
            New message increments message_id
            each user has its own message id correlation
        """
        user = 'users:%s' % username
        # incr user last_message_id
        return app.redis_client.hincrby(user, 'last_message_id', 1)

    def create(**kwargs):
        kwargs['id'] = app.redis_client.incr('last_user_id', amount=1)
        kwargs['active'] = True
        # save user as a hash - users:username
        app.redis_client.hmset('users:%s' % kwargs['username'], kwargs)
        return kwargs


class Bot:
    """ Bot fields: botname, token, id (incremental) """
    @staticmethod
    def get(botname):
        bot = 'bots:%s' % botname
        return app.redis_client.hgetall(bot)

    @staticmethod
    def exists(botname):
        """ Check if bots:<botname> exists """
        return app.redis_client.exists('bots:%s' % botname)

    @staticmethod
    def create(**kwargs):
        kwargs['id'] = app.redis_client.incr('last_bot_id', amount=1)
        # save bot as a hash - bots:botname
        app.redis_client.hmset('bots:%s' % kwargs['botname'], kwargs)
        return kwargs


class Chat:
    """ Chat fields:
            username, botname, active (boolean), id (incremental),
            update_id (incremental for each chat)
    """
    @staticmethod
    def get(id):
        chat = 'chats:%s' % id
        return app.redis_client.hgetall(chat)

    @staticmethod
    def exists(id):
        """ Check if chats:<id> exists """
        return app.redis_client.exists('chats:%s' % id)

    @staticmethod
    def create(**kwargs):
        kwargs['id'] = app.redis_client.incr('last_chat_id', amount=1)
        # save chat as a hash - chats:<chat_id>
        app.redis_client.hmset('chats:%s' % kwargs['id'], kwargs)
        return kwargs

    @staticmethod
    def update(id, field, value):
        """ update/add field with value """
        return app.redis_client.hset('chats:%s' % id, field, value)

    @staticmethod
    def incr_update_id(id):
        """ increments update_id """
        chat = 'chats:%s' % id
        # incr chat update_id
        return app.redis_client.hincrby(chat, 'update_id', 1)
