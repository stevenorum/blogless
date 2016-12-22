#!/usr/bin/env python

from blogless.blogging import BlogPost
from blogless.formatting import format_content
import boto3
import datetime
import json
import sys

ddb = boto3.resource("dynamodb")
table = ddb.Table("blogless_posts")

def get_header_value(header, key, default=None):
    header_lines = header.split("\n")
    for line in header_lines:
        if line.startswith(key + "="):
            return line[len(key) + 1:]
    return default

def boolean_from_string(s):
    if s and type(s) == str and s.lower() in ["y","yes","t","true"]:
        return True
    return False

filename = sys.argv[1]

with open(filename, "r") as f:
    blogfile = f.read()

header, content = blogfile.split("-----content-----\n")


id = get_header_value(header, "id")
title = get_header_value(header, "title", "no title")
timestamp = datetime.datetime.strptime(get_header_value(header, "timestamp"), "%Y-%m-%dZ%H:%M")
published = boolean_from_string(get_header_value(header, "published", "false"))
author = get_header_value(header, "author", "anonymous")


if id:
    existing_post = table.get_item(Key={"post_id":id}).get("Item",None)
    if existing_post:
        print(existing_post)
        raise RuntimeError("Post with ID {id} already exists and updating posts isn't implemented yet.".format(id=id))
    id = int(id)
else:
    response = table.scan(ProjectionExpression="post_id")
    items = response["Items"]
    lastKey = response.get("LastEvaluatedKey", None)
    while lastKey:
        response = table.scan(ProjectionExpression="post_id", ExclusiveStartKey=lastKey)
        items += response["Items"]
        lastKey = response.get("LastEvaluatedKey", None)
    ids = sorted([int(i["post_id"]) for i in items])
    id = 0
    while id in ids:
        id += 1


post = BlogPost(id=id, title=title, content=content, timestamp=timestamp, published=published, author=author)

table.put_item(Item=post.to_dynamo())

