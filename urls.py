from xds_bookmarks import views
from tools.routing import url

urlpatterns = [
    url('/', view_func=views.index),
]
