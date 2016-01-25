from django.apps import AppConfig
from django.db import connection
from django.utils import timezone


def check_and_init_param(**kwargs):
    from xds_server_apps.xds_bookmarks.models import Param, Bookmark

    p = Param.objects.filter(key=kwargs['key']).first()
    if not p:
        p = Param(
            key=kwargs['key'],
            description=kwargs.get('param_description', '')
        )

    parent = kwargs.get('parent', None)
    b = Bookmark.objects.filter(parent=parent, title=kwargs['title']).first()

    if not b:
        b = Bookmark(
            title=kwargs['title'],
            description=kwargs.get('bookmark_description', ''),
            parent=parent,
            position=Bookmark.get_last_position(parent),
            type=kwargs.get('bookmark_type', 2),
            location=kwargs.get('bookmark_location', None),
            date_added=kwargs.get('bookmark_date_added', timezone.now()),
            date_modified=kwargs.get('bookmark_date_modified', timezone.now())
        )
        b.save()

    p.value = str(b.id)
    p.save()


class BookmarksAppConfig(AppConfig):
    name = 'xds_server_apps.xds_bookmarks'
    verbose_name = 'XDS Bookmarks App'

    def ready(self):
        super().ready()
        have_tables = 'xds_bookmarks_param' in connection.introspection.table_names()
        have_tables = have_tables and 'xds_bookmarks_bookmark' in connection.introspection.table_names()
        if not have_tables:
            return

        check_and_init_param(
            key='bookmarks.directory.root',
            param_description='Root directory id.',
            title='Bookmarks',
            bookmark_description='Main directory with bookmarks.'
        )

        check_and_init_param(
            key='bookmarks.directory.front_page',
            param_description='Front page directory id.',
            title='Front Page',
            bookmark_description='Directory with bookmarks that will appear on the front page.'
        )
