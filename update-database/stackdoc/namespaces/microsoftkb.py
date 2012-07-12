import re
import urllib


############### Functions called by stackdoc

def get_version():
    return 1

def get_ids(title, body, tags):
    ids = []
    if "http://support.microsoft.com/":
        urls = re.findall(r'<a href="([^"]+)"', body)
        for url in urls:
            m = re.match("http://support\.microsoft\.com/(?:default\.aspx/)?[kK][bB]/(\w+)", url)
            if m:
                ids.append(m.group(1))
            m2 = re.match("http://support\.microsoft\.com/(?:default\.aspx)?\?scid=[kK][bB];[-\w]+;(\w+)", url)
            if m2:
                ids.append(m2.group(1))

    return ids

def get_tags():
    return None # There isn't a reliable set of tags to filter by. Null indicates that we're not filtering

