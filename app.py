# -*- coding: utf-8 -*-

import os

from flask import Flask

import configuration

app = Flask(__name__)
app.debug = configuration.DEBUG

for application in configuration.APPLICATIONS:
    __import__(application)
    try:
        module_name = '.'.join((application, 'views'))
        __import__(module_name)
    except ImportError as e:
        pass
    else:
        print 'imported: %s' % module_name

for module in os.listdir(os.path.join(configuration.PROJ_DIR, 'utils')):
    if not module.endswith('.py'):
        continue
    module_name = module[:-3]
    try:
        __import__('.'.join(('utils', module_name)))
    except ImportError:
        pass
