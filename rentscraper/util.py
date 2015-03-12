import re

__author__ = 'cdumitru'


def remove_dot(string):
    return string.replace(".", "")


def collapse_whitespace(string):
    return re.sub('\s+', ' ', string)

def has_pp(string):
    if "PP" in string:
        return "yes"
    else:
        return "no"