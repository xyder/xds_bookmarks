from core.routing import url
from xds_bookmarks import views

urlpatterns = [
    url('/', view_func=views.index),
    url('/socks', event_name='xds_bookmarks_get_object', view_func=views.sock_get_object),
    url('/socks', event_name='xds_disconnect', view_func=views.sock_disconnect_request),
    url('/socks', event_name='connect', view_func=views.on_connect),
    url('/socks', event_name='disconnect', view_func=views.on_disconnect),
]
