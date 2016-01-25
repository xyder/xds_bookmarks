from django.conf.urls import url

from xds_server_apps.xds_bookmarks import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
