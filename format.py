#!/usr/bin/env python

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


with open(sys.argv[1],'r') as f:
    content = f.read()

print(format_content(content))
