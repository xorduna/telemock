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
        pass

    @staticmethod
    def incr_user_msg_id(username):
        """
            New message increments message_id
            each user has its own message id correlation
        """
        user = 'users:%s' % username
        # incr user last_message_id
        return app.redis_client.hincrby(user, 'last_message_id', 1)


class Bot:
    """ Bot fields: botname, token, id (incremental) """
    @staticmethod
    def get(botname):
        bot = 'bots:%s' % botname
        return app.redis_client.hgetall(bot)

    @staticmethod
    def exists(botname):
        pass


class Chat:
    """ Chat fields:
            username, botname, active (boolean), id (incremental)
    """
    @staticmethod
    def get(id):
        chat = 'chats:%d' % id
        return app.redis_client.hgetall(chat)

    @staticmethod
    def exists(id):
        pass
