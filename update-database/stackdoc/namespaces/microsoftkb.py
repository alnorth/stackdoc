import re
import urllib


############### Functions called by stackdoc

def get_version():
    return 1

def get_ids(title, body, tags):
    ids = []
    if "http://support.microsoft.com/kb/":
        urls = re.findall(r'<a href="([^"]+)"', body)
        for url in urls:
            m = re.match("http://support\.microsoft\.com/kb/(\w+)", url)
            if m:
                ids.append(m.group(1))

    return ids

def get_tags():
    return None # There isn't a reliable set of tags to filter by. Null indicates that we're not filtering



317535
