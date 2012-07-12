import re
import urllib


############### Functions called by stackdoc

def get_version():
    return 2

def get_ids(title, body, tags):
    ids = []
    if "http://docs.python.org/" in body:
        urls = re.findall(r'<a href="([^"]+)"', body)
        for url in urls:
            m = re.match("http://docs.python.org/(?:release/)?(?:dev/)?(?:[0-9](?:\.[0-9]/)+)?(?:py3k/)?library/([.a-z0-9]+)(?:-examples)?\.html", url)
            if m:
                ids.append(m.group(1))
    if "http://www.python.org/doc/" in body:
        urls = re.findall(r'<a href="([^"]+)"', body)
        for url in urls:
            m = re.match("http://www.python.org/doc/(?:[0-9](?:\.[0-9]/)+)/lib/module-([.a-z0-9]+)\.html", url)
            if m:
                ids.append(m.group(1))

    return ids

def get_tags():
    return [
        "python"
    ]
