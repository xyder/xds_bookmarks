from flask import render_template


def index():
    """
    The index view for the bookmarks app.
    """

    return render_template('xds_bookmarks/index.html')
