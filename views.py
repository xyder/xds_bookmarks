import logging

from flask import render_template, request
from flask.ext.socketio import emit, disconnect


def index():
    """
    The index view for the bookmarks app.
    """

    return render_template('xds_bookmarks/index.html')


def sock_get_object(message):
    print(message)
    print(type(message))


def sock_disconnect_request():
    # noinspection PyUnresolvedReferences
    emit('xds_connection_event', {'data': 'disconnected', 'sid': request.sid})
    disconnect()


def on_connect():
    # noinspection PyUnresolvedReferences
    emit('xds_connection_event', {'data': 'connected', 'sid': request.sid})


def on_disconnect():
    # noinspection PyUnresolvedReferences
    print('Client [%s] disconnected.' % request.sid)
