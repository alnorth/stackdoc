import re
import urllib


############### Functions called by stackdoc

def get_version():
    return 1

def get_ids(title, body, tags):
    ids = []
    if "http://java.sun.com/" in body or "http://docs.oracle.com/":
        urls = re.findall(r'<a href="([^"]+)"', body)
        for url in urls:
            m = re.match("http://(?:java\.sun|docs\.oracle)\.com/(?:javase|j2se|javaee|j2ee)/\d(?:\.\d)*/docs/api/(\w+(?:/\w+)*)\.html", url)
            if m:
                ids.append(m.group(1).replace("/", "."))

    return ids

def get_tags():
    return [
        "java",
        "java-ee"
    ]
