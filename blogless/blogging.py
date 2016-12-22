#!/usr/bin/env python

from datetime import datetime
from formatting import format_content

class BlogPost(object):
    """docstring for BlogPost."""
    def __init__(self, id, title, content, timestamp, newer=None, older=None, published=True, author=None):
        super(BlogPost, self).__init__()
        self.id = id
        self.title = title
        self.content = format_content(content)
        self.timestamp = timestamp
        self.newer = newer
        self.older = older
        self.published = published
        self.author = author

    @property
    def day(self):
        return self.timestamp.strftime("%Y-%m-%d")

    def to_dynamo(self):
        return {
            "post_id":str(self.id),
            "post_title":self.title,
            "post_content":self.content,
            "publish_timestamp":datetime.strftime(self.timestamp,"%Y-%m-%dZ%H:%M"),
            "published":self.published,
            "author":self.author
            }

    @classmethod
    def from_dynamo(cls, dynamo):
        post = cls(
            id=dynamo["post_id"],
            title=dynamo["post_title"],
            content=dynamo["post_content"],
            timestamp=datetime.strptime(dynamo["publish_timestamp"],"%Y-%m-%dZ%H:%M"),
            published=dynamo.get("published", False),
            author=dynamo.get("author", None)
            )
        return post
