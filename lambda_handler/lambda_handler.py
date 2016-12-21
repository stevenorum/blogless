#!/usr/bin/env python

import boto3
from formatting import format_content
import json

ddb = boto3.resource("dynamodb")
config_table = ddb.Table("blogless_config")
posts_table = ddb.Table("blogless_posts")

def lambda_handler(event, context):
    # NOTE: need to url-encode ampersands to %26 when passing stuff as a subparam of bl
    #print(event)
    path=event["bl"]
    parts = path.split("?")
    querystring = "?".join(parts[1:]) if len(parts) > 1 else ""
    qs_params = []
    if querystring:
        for qp in querystring.split("&"):
            segments = qp.split("=")
            q1 = segments[0]
            q2 = "=".join(segments[1:]) if len(segments) > 1 else None
            pair = (q1,q2)
            qs_params.append(str(pair))
    path = parts[0]
    path_elements = path.split("/")
    content = "RAW BL: " + event["bl"] + "\n"
    content += "RAW PATH: " + path + "\n"
    content += "RAW QS: " + querystring + "\n"
    content += "PATH ELEMENTS: " + ", ".join(path_elements) + "\n"
    content += "QUERYSTRING PARAMS: " + ", ".join(qs_params) + "\n"
#    querystring = path.split("?")
#    parts[-1] = parts[]
#    content = json.dumps(event, indent=2)
    #content += "\n" + str(dir(context))
#    content += "\n" + str(context.client_context)
    content = format_content(content)
    print(content)
    #return fake_html.format(content="")
    return fake_html.format(content=content)

base_params = {
"title":"",
"author":""
}

index_params = {
"blogposts":[]
}

post_params = {
"post":None
}

fake_html = """<html><head><title>HTML from API Gateway/Lambda</title></head><body><h1>HTML from API Gateway/Lambda</h1>{content}</body></html>"""

base_html = open("templates/base.html",'r').read()

post_html = open("templates/post.html",'r').read()

index_html = open("templates/index.html",'r').read()
