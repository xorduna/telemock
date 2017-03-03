#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_restful import Api

import redis
import logging.handlers

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
        if request.form:
            app.logger.info(request.form)
            app.logger.info(request.files)
        else:
            app.logger.info(request.data)

    @app.after_request
    def after_request(response):
        app.logger.info(response.data)
        return response

def setup_redis(app):
    pool = redis.ConnectionPool.from_url(
        app.config['REDIS_URI'], decode_responses=True)
    app.redis_client = redis.Redis(connection_pool=pool)

def setup_app():
    app = Flask(__name__)
    app.config.from_object('settings')

    setup_redis(app)
    setup_logger(app)

    return app

if __name__ == '__main__':
    from api import UserApi, BotApi, ChatApi, ChatByIdApi, ChatMessage
    from bot_api import (
        SendMessage, SendPhoto, SendDocument,
        SendVideo, SendAudio, SendChatAction)

    # start telegram mock api server
    app = setup_app()
    # register api endpoints
    api = Api(app)

    # register internal api endpoints
    api.add_resource(UserApi, '/user')
    api.add_resource(BotApi, '/bot')
    api.add_resource(ChatApi, '/chat')
    api.add_resource(ChatByIdApi, '/chat/<chat_id>')
    api.add_resource(ChatMessage, '/chat/<chat_id>/message')

    # register bot api endpoints
    api.add_resource(SendMessage, '/sendMessage')
    api.add_resource(SendChatAction, '/SendChatAction')

    api.add_resource(SendPhoto, '/SendPhoto')
    api.add_resource(SendDocument, '/SendDocument')
    api.add_resource(SendVideo, '/SendVideo')
    api.add_resource(SendAudio, '/SendAudio')

    app.run()
