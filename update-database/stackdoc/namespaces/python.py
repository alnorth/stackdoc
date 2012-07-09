import re
import urllib


############### Functions called by stackdoc

def get_version():
    return 2

def get_ids(title, body, tags):
    ids = []
    if "http://docs.python.org/" in body or "http://www.python.org/doc/" in body:
        urls = re.findall(r'<a href="([^"]+)"', body)
        for url in urls:
            docsm = re.match("http://docs.python.org/(?:release/)?(?:dev/)?(?:[0-9](?:\.[0-9]/)+)?(?:py3k/)?library/([.a-z0-9]+)(?:-examples)?\.html", url)
            if docsm:
                ids.append(docsm.group(1))
            olddocsm = re.match("http://www.python.org/doc/(?:[0-9](?:\.[0-9]/)+)/lib/module-([.a-z0-9]+)\.html", url)
            if olddocsm:
                ids.append(olddocsm.group(1))

    return ids

def get_tags():
    return [
        "python"
    ]
