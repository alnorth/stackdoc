import re
import urllib


############### Functions called by stackdoc

def get_version():
    return 1

def get_ids(title, body, tags):
    ids = []
    if "http://docs.python.org/" in body:
        pass
    return ids

def get_tags():
    return [
        "python"
    ]
