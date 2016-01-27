from django.contrib import admin
from xds_server_apps.xds_bookmarks.models import Bookmark, Location, Param, Page, Pane, Tab

admin.site.register(Bookmark)
admin.site.register(Location)
admin.site.register(Param)
admin.site.register(Page)
admin.site.register(Pane)
admin.site.register(Tab)
