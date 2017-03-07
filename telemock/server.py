#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_restful import Api

import redis
import logging.handlers

#import api
#import bot_api

#from api import UserApi, BotApi, ChatApi, ChatByIdApi, ChatMessage

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

    lua_script = """
        local collate = function (key)
            local raw_data = redis.call('HGETALL', key)
            local data = {}

            for idx = 1, #raw_data, 2 do
                data[raw_data[idx]] = raw_data[idx + 1]
            end

            return data
        end

        local data = {}

        for _, key in pairs(KEYS) do
            data[#data+1] = collate(key)
        end

        return cjson.encode(data)
    """
    app.hgetall_keys = app.redis_client.register_script(lua_script)

def setup_app():
    app = Flask(__name__)
    app.config.from_object('settings')

    setup_redis(app)
    #setup_logger(app)

    @app.route("/")
    def home():
        return 'this is telemock :)!'

    return app

def create_app():
    app = setup_app()

    from api import UserApi, BotApi, ChatApi, ChatMessage
    from bot_api import (
        SendMessage, GetUpdates, SendPhoto, SendDocument,
        SendVideo, SendAudio, SendChatAction, SetWebhook)

    api = Api(app)

    api.add_resource(UserApi, '/user', '/user/<username>')
    api.add_resource(BotApi, '/bot', '/bot/<botname>')
    api.add_resource(ChatApi, '/chat', '/chat/<chat_id>')
    api.add_resource(ChatMessage, '/chat/<chat_id>/message')

    # register bot api endpoints
    api.add_resource(SendMessage, '/bot<token>/sendMessage')
    api.add_resource(SetWebhook, '/bot<token>/setWebhook')
    api.add_resource(SendChatAction, '/bot<token>/sendChatAction')
    api.add_resource(GetUpdates, '/bot<token>/getUpdates')

    api.add_resource(SendPhoto, '/bot<token>/sendPhoto')
    api.add_resource(SendDocument, '/bot<token>/sendDocument')
    api.add_resource(SendVideo, '/bot<token>/sendVideo')
    api.add_resource(SendAudio, '/bot<token>/sendAudio')

    return app

if __name__ == '__main__':

    app = create_app()

    app.run(host="0.0.0.0")
