from django.contrib import admin
from xds_server_apps.xds_bookmarks.models import Bookmark, Location, Param

admin.site.register(Bookmark)
admin.site.register(Location)
admin.site.register(Param)
