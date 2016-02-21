from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, backref

from core.database import Base
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

    type = Column(Enum('container', 'item', name='bookmark_types'), nullable=False)

    location_id = Column(Integer, ForeignKey(prefixer('locations.id')), index=True)
    location = relationship('Location', backref='bookmarks')

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

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


# register recounting listeners for these models
Base.register_recountable_model(Bookmark)
