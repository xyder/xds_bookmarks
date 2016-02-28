from flask import render_template, request
from flask.ext.socketio import emit, disconnect

from server import settings


def index():
    """
    The index view for the bookmarks app.
    """

    return render_template('xds_bookmarks/index.html')


def sock_get_object(message):
    logger = settings.get_logger()
    logger.info('%s - received: %s' % (getattr(request, 'sid'), message))


def sock_disconnect_request():
    emit('xds_connection_event', {'data': 'disconnected', 'sid': getattr(request, 'sid', '')})
    disconnect()


def on_connect():
    emit('xds_connection_event', {'data': 'connected', 'sid': getattr(request, 'sid', '')})


def on_disconnect():
    logger = settings.get_logger()
    logger.info('%s - client disconnected.' % getattr(request, 'sid', ''))
