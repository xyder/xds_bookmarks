from xds_server.core.lib import create_admin_view
from xds_server_apps.xds_bookmarks import models

create_admin_view(models.Location)
create_admin_view(models.Bookmark)
create_admin_view(models.Page)
create_admin_view(models.Pane)
create_admin_view(models.Tab)
