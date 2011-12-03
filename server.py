#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import configuration
import optparse

sys.path.insert(0, configuration.PROJ_DIR)



def start_server(address='localhost:8000'):
    from gevent.wsgi import WSGIServer
    from app import app

    host, port = address.split(':')
    port = int(port)
    http_server = WSGIServer((host, port), app)
    print 'server started:   http://%s:%s\n' % (host, port)
    http_server.serve_forever()



def main():
    parser = optparse.OptionParser('usage: %prog <params>')
    parser.add_option('-r', '--run-server', dest='run_server',
            action='store_true')
    (options, args) = parser.parse_args()
    if options.run_server:
        start_server(*args)
    

if __name__ == '__main__':
    main()
