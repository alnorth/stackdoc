import json
from pymongo import Connection
import re
import urllib

connection = Connection()
db = connection.stack_doc
posts = db.posts

for id in posts.distinct("page_ids"):
    if re.search("^[a-zA-Z0-9]{8}$", id):
        handle = urllib.urlopen("http://msdnid.alnorth.com/" + id)
        print "%s - %s" % (id, handle.readline())

