__author__ = 'cdumitru'


def remove_dot(string):
    return string.replace(".", "")


def has_pp(string):
    if "PP" in string:
        return "yes"
    else:
        return "no"