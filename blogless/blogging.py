#!/usr/bin/env python

from datetime import datetime
from formatting import format_content

BLOG_POST_404 = """
The No To Ich Way of strategy is recorded in this the Book of the Void.

What is called the spirit of the void is where there is nothing. It is not included in man's knowledge. Of course the void is nothingness. By knowing things that exist, you can know that which does not exist. That is the void.

People in this world look at things mistakenly, and think that what they do not understand must be the void. This is not the true void. It is bewilderment.

In the Way of strategy as a warrior you must study fully other martial arts and not deviate even al little from the Way of the warrior. With your spirit settled, accumulate practice day by day, hour by hour. Polish the twofold spirit heart and mind, and sharpen the twofold gaze perception and sight. When your spirit is not in the least clouded, when the clouds of bewilderment clear away, there is the true void.

Until you realize the true Way, whether in Buddhism or in common sense, you may think that things are correct and in order. However, if we look at things objectively, from the viewpoint of laws of the world, we see various doctrines departing from the true Way. Know well this spirit, and with forthrightness as the foundation and the true spirit as the Way. Enact strategy broadly, correctly and openly.

Then you will come to think of things in a wide sense and, taking the void as the Way, you will see the Way as void.

In the void is virtue, and no evil. Wisdom has existence, principle has existence, the Way has existence, spirit is nothingness.
"""

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

    @property
    def public(self):
        return self.published and datetime.now() > self.timestamp

    def to_dynamo(self):
        if self.id == "-1":
            return None
        return {
            "post_id":str(self.id),
            "post_title":self.title,
            "post_content":self.content,
            "publish_timestamp":datetime.strftime(self.timestamp,"%Y-%m-%dZ%H:%M"),
            "published":self.published,
            "author":self.author
            }

    @classmethod
    def from_dynamo(cls, dynamo, ignore_failure=True):
        try:
            post = cls(
                id=dynamo["post_id"],
                title=dynamo["post_title"],
                content=dynamo.get("post_content", ""),
                timestamp=datetime.strptime(dynamo["publish_timestamp"],"%Y-%m-%dZ%H:%M"),
                published=dynamo.get("published", False),
                author=dynamo.get("author", None)
                )
            return post
        except Exception as e:
            if ignore_failure:
                return None
            raise e

    @classmethod
    def not_found(cls):
        post = cls(
            id="-1",
            title="My thoughts on HTTP status code 404",
            content=BLOG_POST_404,
            timestamp=datetime.now(),
            published=True,
            author="Miyamoto Musashi"
            )
        return post
