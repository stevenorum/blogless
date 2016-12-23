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

def catchall(event, context):
    event = event if type(event) == dict else json.loads(event)

    path = event["path"]
    path_params = event["pathParameters"]
    resource = event["resource"]
    qsp = event["queryStringParameters"]
    method = event["httpMethod"]
    request_body = event["body"]

    content = "Path: {path}\nPath Params: {path_params}\nResource: {resource}\nQS Params: {qsp}\nHTTP Method: {method}\nRequest body: {request_body}".format(
        path = path,
        path_params = json.dumps(path_params, sort_keys=True),
        resource = resource,
        qsp = json.dumps(qsp, sort_keys=True),
        method = method,
        request_body = request_body if request_body else ""
        )

    params = base_params.copy()
    params["landing_page"] = format_content(content)

    template = env.get_template('index.html')
    body = template.render(**params)

    response = {}
    response["statusCode"] = 200
    response["body"] = body
    response["headers"]  = {"Content-Type": "text/html"}
    return response

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
    params["post"] = load_blogpost(event["identifier"], fancy404=True)
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
    projection = "post_id, post_title, published, publish_timestamp"
    response = posts_table.scan(ProjectionExpression=projection)
    items = response["Items"]
    lastKey = response.get("LastEvaluatedKey", None)
    while lastKey:
        response = posts_table.scan(ProjectionExpression=projection, ExclusiveStartKey=lastKey)
        items += response["Items"]
        lastKey = response.get("LastEvaluatedKey", None)
    blogposts = [BlogPost.from_dynamo(e, ignore_failure=False) for e in items]
    blogposts = [bp for bp in blogposts if bp.public]
    blogposts.sort(key=lambda x: x.timestamp, reverse=True)
    for i in range(len(blogposts)):
        if (i-1) >= 0:
            blogposts[i].newer = blogposts[i-1]
        if (i+1) < len(blogposts):
            blogposts[i].older = blogposts[i+1]
    return blogposts

def load_blogpost(id, fancy404=False):
    item = posts_table.get_item(Key={"post_id":id}).get("Item",None)
    if item:
        bp = BlogPost.from_dynamo(item)
        if bp.public:
            return bp
    if fancy404:
        return BlogPost.not_found()
    else:
        return None


static_cache = {}

base_params = {
"title":"Blogless",
"author":"Steve Norum"
}
