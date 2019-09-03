import handlers

from sneks.sam.response_core import PathMatcher, ListMatcher, ResponseException, get_matchers
from sneks.sam import ui_stuff

STATIC_MATCHERS = [
    PathMatcher(r"^.*/favicon.ico$", ui_stuff.get_static, {"filename":"static/favicon.ico"}),
    PathMatcher(r"^/?(?P<filename>static/.*)$", ui_stuff.get_static),
]

STANDARD_PREPROCESSORS = [
    handlers.add_qs_as_kwargs
]

API_PREPROCESSORS = [
    handlers.add_body_as_kwargs
]

HTML_MATCHERS = get_matchers("HTML", preprocessor_functions=STANDARD_PREPROCESSORS)
API_MATCHERS = get_matchers("API", preprocessor_functions=STANDARD_PREPROCESSORS + API_PREPROCESSORS)

DEFAULT_MATCHERS = [
    PathMatcher(r"^/?$", ui_stuff.get_page, {"template_name":"index.html"}, preprocessor_functions=STANDARD_PREPROCESSORS),
    PathMatcher(r"^/?(?P<template_name>[a-z_]*.html)$", ui_stuff.get_page, preprocessor_functions=STANDARD_PREPROCESSORS),
    PathMatcher(r".*debug.*", ui_stuff.make_debug, preprocessor_functions=STANDARD_PREPROCESSORS),
    PathMatcher(r".*", ui_stuff.make_404)
]

MATCHERS = ListMatcher(STATIC_MATCHERS + HTML_MATCHERS + API_MATCHERS + DEFAULT_MATCHERS)

def lambda_handler(event, context):
    try:
        return MATCHERS.handle_event(event)
    except ResponseException as e:
        return e.response
