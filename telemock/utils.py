#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def env_setting(setting_name, default=''):
    """ Fetch setting value from env, if not exist take default """
    if os.environ.get(setting_name):
        return os.environ[setting_name]
    return default
