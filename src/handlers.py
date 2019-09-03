import base64
import boto3
import copy
from datetime import datetime, timedelta
from decimal import Decimal
import hashlib
import http.cookies
import json
from math import radians, degrees, cos, sin, asin, sqrt, fabs, log, tan, pi, atan2
import os
import random
import traceback
import urllib
import urllib.parse
import uuid
import time

from sneks.sam import events
from sneks.sam.response_core import make_response, redirect, ApiException
from sneks.sam.decorators import register_path, returns_json, returns_html
from sneks.sam.exceptions import *
from sneks.ddb import deepload

def sanitize(s):
    return s.replace('"',"")

@register_path("HTML", r"^/?$")
@returns_html("index.html")
def catchall_page(event, *args, **kwargs):
    return {}

def get_cookies(event):
    cookie_dict = {}
    try:
        cookies = http.cookies.SimpleCookie()
        cookies.load(event["headers"].get("Cookie",""))
        for k in cookies:
            morsel = cookies[k]
            cookie_dict[morsel.key] = morsel.value
    except:
        traceback.print_exc()
    return cookie_dict

def _add_info_kwargs(info, kwargs):
    if not kwargs:
        return info
    existing_kwargs = list(info.keys())
    for k in kwargs:
        if k not in existing_kwargs:
            info[k] = kwargs[k]
    return info

def add_body_as_kwargs(info, *args, **kwargs):
    if not info["event"].get("body"):
        info["body"] = {}
        return info
    body = json.loads(info["event"]["body"])
    info["body"] = body
    return _add_info_kwargs(info, body)

def add_qs_as_kwargs(info, *args, **kwargs):
    qs_args = info["event"]["queryStringParameters"]
    info["qs_args"] = qs_args
    return _add_info_kwargs(info, qs_args)
