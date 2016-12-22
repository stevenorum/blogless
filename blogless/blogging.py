#!/usr/bin/env python

from formatting import format_content

class BlogPost(object):
    """docstring for BlogPost."""
    def __init__(self, id, title, content, timestamp, newer=None, older=None):
        super(BlogPost, self).__init__()
        self.id = id
        self.title = title
        self.content = format_content(content)
        self.timestamp = timestamp
        self.newer = newer
        self.older = older

    @property
    def day(self):
        return self.timestamp.strftime("%Y-%m-%d")
