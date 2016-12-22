#!/usr/bin/env python

from blogging import BlogPost
import boto3
import datetime
from formatting import format_content
from jinja2 import Environment, FileSystemLoader
import json

ddb = boto3.resource("dynamodb")
posts_table = ddb.Table("blogless_posts")

env = Environment(loader=FileSystemLoader('templates'))

def landing_page(event, context):
    event = event if type(event) == dict else json.loads(event)
    params = base_params.copy()
    params["landing_page"] = format_content("This is some basic landing-page content.")
    params["blogposts"] = load_blogposts()
    template = env.get_template('index.html')
    return template.render(**params)

def view_post(event, context):
    event = event if type(event) == dict else json.loads(event)
    params = base_params.copy()
    params["post"] = load_blogpost(event["identifier"])
    template = env.get_template('post.html')
    return template.render(**params)

def load_static(event, context):
    event = event if type(event) == dict else json.loads(event)
    filename = event["filename"]
    if filename in static_cache:
        return static_cache[filename]
    with open(filename, "r") as f:
        content = f.read()
    static_cache[filename] = content
    return content

def load_blogposts():
    response = posts_table.scan(
    IndexName="post_timestamp_index",
    Select="ALL_PROJECTED_ATTRIBUTES"
    )
    newest = BlogPost(id="2", title="Newest blog post",content="Some blog content goes here.\nAnd also here.",timestamp=datetime.datetime(2016,12,21,21,21))
    oldest = BlogPost(id="1", title="Oldest blog post",content="Some blog content goes here.\nAnd also here.",timestamp=datetime.datetime(2016,12,1,1,1))
    middle = BlogPost(id="0", title="Middle blog post",content="Some blog content goes here.\nAnd also here.",timestamp=datetime.datetime(2016,12,11,11,11), older=oldest, newer=newest)
    newest.older = middle
    oldest.newer = middle
    return [newest, middle, oldest]

def load_blogpost(id):
    return {post.id:post for post in load_blogposts()}.get(id, None)

static_cache = {}

base_params = {
"title":"Blogless",
"author":"Steve Norum"
}
