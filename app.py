# -*- coding: utf-8 -*-

import os

from flask import Flask

import configuration

app = Flask(__name__)

def app(env, start_response):
    """Another example application for gevent wsgi server"""
    if env['PATH_INFO'] == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return ["<b>hello world</b>"]
    else:
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return ['<h1>Not Found</h1>']


def app(environment, start_response):
    """Yet another example application for gevent wsgi server"""
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    print 'in app'
    return ["hello, world!"]

app.debug = configuration.DEBUG

# Import applications into namespace
for application in configuration.APPLICATIONS:
    __import__('.'.join(configuration.APPS_DIR, application))
    try:
        module_name = '.'.join((application, 'views'))
        __import__(module_name)
    except ImportError as e:
        pass
    else:
        print 'imported: %s' % module_name

# Import utils into namespace
for module in os.listdir(os.path.join(configuration.PROJ_DIR, 'utils')):
    if not module.endswith('.py'):
        continue
    module_name = module[:-3]
    try:
        __import__('.'.join(('utils', module_name)))
    except ImportError:
        pass
