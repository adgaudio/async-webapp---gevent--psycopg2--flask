#!/usr/bin/env python
""" Create a ZMQ Server using Gevent"""

from gevent import spawn
from gevent_zeromq import zmq


def serve(socket):
    """Receive and handle requests.  Send response."""
    while True:
        request = socket.recv()

        # Handle request here
        response = request

        socket.send(response)


def start_serving():
    """Setup ZMQ context, bind to socket, and start server"""
    context = zmq.Context()
    sock = context.socket(zmq.REP)
    sock.bind('tcp://127.0.0.1:5000')
    print "Starting Server on socket: %s" % sock
    server = spawn(serve, sock)



if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser('usage: %prog <params>')
    parser.add_option('-r', '--run-server', dest='run_server',
            action='store_true')
    (options, args) = parser.parse_args()

    if options.run_server:
        start_serving()

        # An example client communication
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://127.0.0.1:5000")
        def client():
            for request in range(1,10):
                socket.send("Hello")
                message = socket.recv()
                print "Received reply ", request, "[", message, "]"
        spawn(client).join()
