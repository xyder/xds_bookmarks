from flask.ext.admin.contrib.sqla import ModelView

from xds_server.core import admin
from xds_server.core.database import db_session
from xds_server_apps.xds_bookmarks import models

admin.add_view(ModelView(models.Location, db_session))
admin.add_view(ModelView(models.Bookmark, db_session))
admin.add_view(ModelView(models.Page, db_session))
admin.add_view(ModelView(models.Tab, db_session))
admin.add_view(ModelView(models.Pane, db_session))
