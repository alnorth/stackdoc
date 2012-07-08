import re
import urllib


############### Functions called by stackdoc

def get_version():
    return 1

def get_ids(title, body, tags):
    ids = []
    if "http://www.python.org/" in body:
        urls = re.findall(r'<a href="([^"]+)"', body)
        for url in urls:
            m = re.match("http:\/\/www\.python\.org\/dev\/peps\/pep\-([0-9]+)", url)
            if m:
                ids.append(m.group(1))
    return ids

def get_tags():
    return [
        "python"
    ]
