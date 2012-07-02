import re
import urllib


############### Functions called by stackdoc

def get_name():
    return "jquery"

def get_version():
    return 1

def get_ids(title, body, tags):
    ids = []
    if "http://api.jquery.com/" in body:
        matches =  re.findall(r"http://api\.jquery\.com/([.\-a-zA-Z0-9]+)/?", body)
        for match_id in matches:
            ids.append(match_id)
    return ids

def get_tags():
    return [
        "javascript",
        "jquery"
    ]
