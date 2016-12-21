#!/usr/bin/env python

import boto3
import json

ddb = boto3.resource("dynamodb")
config_table = ddb.Table("blogless_config")
posts_table = ddb.Table("blogless_posts")

['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'aws_request_id', 'client_context', 'function_name', 'function_version', 'get_remaining_time_in_millis', 'identity', 'invoked_function_arn', 'log', 'log_group_name', 'log_stream_name', 'memory_limit_in_mb', 'xray_context']

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

base_html = """
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <meta name="author" content="{{author}}" />
  <meta name="viewport" content="width=device-width">
  <title>{{title}}</title>
  <link rel="stylesheet" href="style.css" type="text/css" charset="utf-8">
</head>

<body>
{% block body %}{% endblock %}
</body>
</html>
"""

post_html = """
{% extends "base.html" %}
{% block body %}
<h2><a href="index.html">[back to stevenorum.com]</a></h2>
<h2>{{post.day}}: {{post.title}} {% if post.newer %}<a href="posts?id={{post.newer.id}}">>>[newer post]</a>{% endif %} {% if post.older %}<a href="posts?id={{post.older.id}}">>>[older post]</a>{% endif %}</h2>
{{content}}
{% endblock %}
"""

index_html = """
{% extends "base.html" %}
{% block body %}
{{landing_page}}

<h2>
  Blog posts
</h2>
<ul>
    {% for post in blogposts %}
    <li><a href="posts?id={{post.id}}">>>[{{post.day}}] {{post.title}}</a></li>
    {% endfor %}
</ul>
{% endblock %}
"""

import re
import sys

LEADING_WS_RE = re.compile(r"^\s+")
WS_RE = re.compile(r"\s+")

def LEADING_WS_CONVERTER(s, match):
    return s[:match.start()] + match.group().replace('\t','    ').replace(' ','&nbsp;') + s[match.end():]

def WS_CONVERTER(s, match):
    group = match.group().replace('\t','    ')
    return s[:match.start()] + ' ' + match.group().replace('\t','    ')[1:].replace(' ','&nbsp;') + s[match.end():]

def get_all_matches(s, regex):
    matches = []
    end = 0
    while end < len(s)-1:
        match = regex.search(s, pos=end)
        if match:
            matches = [match] + matches
            end = match.end()
        else:
            end = len(s)
    return matches

def replace(s, regex, converter):
    matches = get_all_matches(s, regex)
    for match in matches:
        s = converter(s, match)
    return s

def format_line(line):
    line = replace(line, LEADING_WS_RE, LEADING_WS_CONVERTER)
    line = replace(line, WS_RE, WS_CONVERTER)
    if line:
        line = line + "<br>"
    else:
        line = '\n'
    return line

def format_content(content):
    lines = content.split('\n')
    lines = [format_line(line) for line in lines]
    content = ''.join(lines)
    paragraphs = content.split('\n')
    content = '\n'.join('<p>' + p + '</p>' for p in paragraphs)
    content = content.replace('<br>','<br>\n')
    return content
