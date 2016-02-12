from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.event import listen

from core.database import Base, db_session
from core.lib import get_custom_prefixer
from xds_bookmarks import APP_NAME


prefixer = get_custom_prefixer(APP_NAME)


class Location(Base):
    """
    Model for URL.
    """

    __tablename__ = prefixer('locations')

    id = Column(Integer, primary_key=True)
    url = Column(Text, nullable=True)

    def __repr__(self):
        return self.url


class Bookmark(Base):
    """
    Self-referencing model for Bookmarks.
    """

    __tablename__ = prefixer('bookmarks')

    id = Column(Integer, primary_key=True)

    parent_id = Column(Integer, ForeignKey(prefixer('bookmarks.id')), index=True)
    parent = relationship('Bookmark',
                          remote_side=[id],
                          backref=backref('children', cascade='all,delete'))

    position = Column(Integer)

    title = Column(Text)
    description = Column(Text)

    date_added = Column(DateTime)
    date_modified = Column(DateTime)

    type = Column(Enum("container", "item", name='bookmark_types'), nullable=False)

    location_id = Column(Integer, ForeignKey(prefixer('locations.id')), index=True)
    location = relationship('Location', backref='bookmarks')

    def __repr__(self):
        return self.title


class Page(Base):
    """
    Model for Page. This would correspond to an actual page on the web interface.
    """

    __tablename__ = prefixer('pages')

    id = Column(Integer, primary_key=True)
    title = Column(Text)

    def __repr__(self):
        return self.title


class Tab(Base):
    """
    Model for a Tab. Multiple tabs can be part of a page.
    """

    __tablename__ = prefixer('tabs')

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    page_id = Column(Integer, ForeignKey(prefixer('pages.id')), index=True)
    page = relationship('Page', backref='tabs')

    def __repr__(self):
        return self.title


class Pane(Base):
    """
    Model for a Pane. Multiple panes can be part of a tab. A pane can have a bookmark directory associated.
    """

    __tablename__ = prefixer('panes')

    id = Column(Integer, primary_key=True)

    bookmark_id = Column(ForeignKey(prefixer('bookmarks.id')), index=True, nullable=False)
    bookmark = relationship('Bookmark', backref='pane', uselist=False)

    width = Column(Integer, default=0)
    height = Column(Integer, default=0)

    x = Column(Integer, default=0)
    y = Column(Integer, default=0)

    tab_id = Column(ForeignKey(prefixer('tabs.id')), index=True)
    tab = relationship('Tab', remote_side=[Tab.id], backref='panes')

    def __repr__(self):
        return '{"id": "%s", "bookmark_id": "%s"}' % (self.id, self.bookmark_id)


def recount_positions(bookmark, is_deleted):
    """
    Function that recounts the relative positions of the children of the parent of the given bookmark.
    :param is_deleted: if the bookmark is marked for deletion.
    """

    children = Bookmark.query.filter(
        Bookmark.parent == bookmark.parent
    ).order_by(Bookmark.position.asc()).all()

    if bookmark in children:
        children.remove(bookmark)

    k = 0
    n = len(children)

    if not is_deleted:
        if bookmark.position is None or bookmark.position > n:
            bookmark.position = n

        if bookmark.position < 0:
            bookmark.position = 0

    for child in children:
        # skip bookmark if not deleted
        if k == bookmark.position and not is_deleted:
            k += 1

        child.position = k
        k += 1


def process_session_objects(session, objects, parents, is_deleted):
    """
    Function that processes a set of session objects.
    :param parents: the bookmark parents for which the children were already recounted.
    :param is_deleted: if the objects in the set were marked for deletion
    :return: expanded list of parents for which the children were recounted.
    """

    for obj in objects:
        if isinstance(obj, Bookmark) and obj.parent not in parents:
            if session.is_modified(obj) or is_deleted:
                recount_positions(obj, is_deleted)
                parents.append(obj.parent)
    return parents


# listeners
# noinspection PyUnusedLocal
def before_session_flush(session, flush_context, instances):
    """
    Function that processes session objects before they are stored in the database.
    """

    parents = []
    parents = process_session_objects(session, session.new, parents, False)
    parents = process_session_objects(session, session.dirty, parents, False)
    process_session_objects(session, session.deleted, parents, True)


# listener registration
listen(db_session, 'before_flush', before_session_flush)
