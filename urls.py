from core.routing import url
from xds_bookmarks import views

urlpatterns = [
    url('/', view_func=views.index),
]

socketpatterns = [
    url('/socks', routes=[
        url(event_name='xds_bookmarks_get_object', socket_func=views.sock_get_object),
        url(event_name='xds_disconnect', socket_func=views.sock_disconnect_request),
        url(event_name='connect', socket_func=views.on_connect),
        url(event_name='disconnect', socket_func=views.on_disconnect),
    ])
]
