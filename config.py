#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 sw=4 ts=4 et:


# general
DEBUG = False
PATH = '/var/www/html/example.com/ffa/'

try:
    from local_config import *
except ImportError:
    # no local config found
    pass
