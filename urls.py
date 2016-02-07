from xds_server_apps.xds_bookmarks import views
from xds_server.tools.routing import url

urlpatterns = [
    url('/', view_func=views.index),
]
