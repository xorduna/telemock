#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_restful import Api

import redis
import logging.handlers

from api import User, Bot, Chat, ChatById
from bot_api import SendMessage

def setup_logger(app):
    handler = logging.handlers.WatchedFileHandler(app.config['LOG_FILE'])
    handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))

    app.logger.setLevel(app.config['LOG_LEVEL'])
    app.logger.addHandler(handler)

    @app.before_request
    def before_request():
        app.logger.info("{method} {url}".format(
            method=request.method, url=request.url)
        )
        app.logger.info(request.data)

    @app.after_request
    def after_request(response):
        app.logger.info(response.data)
        return response

def setup_redis(app):
    pool = redis.ConnectionPool.from_url(app.config['REDIS_URI'])
    app.redis_client = redis.Redis(connection_pool=pool)

if __name__ == '__main__':
    # start telegram mock api server
    app = Flask(__name__)
    app.config.from_object('settings')

    setup_redis(app)
    setup_logger(app)
    # register api endpoints
    api = Api(app)

    # register internal api endpoints
    api.add_resource(User, '/user')
    api.add_resource(Bot, '/bot')
    api.add_resource(Chat, '/chat')
    api.add_resource(ChatById, '/chat/<chat_id>')

    # register bot api endpoints
    api.add_resource(SendMessage, '/SendMessage')

    app.run()
