import json
from pymongo import Connection
import re
import urllib

connection = Connection()
db = connection.stack_doc
posts = db.posts

i = 1
ids = posts.distinct("page_ids")

for id in ids:
    if re.search("^[a-zA-Z0-9]{8}$", id):
        handle = urllib.urlopen("http://msdnid.alnorth.com/" + id)
        if handle.getcode() == 200:
            canonical = handle.readline()
            print "%i/%i - %s - %s" % (i, len(ids), id, canonical)
            posts.update({"page_ids": id}, {"$addToSet": {"page_ids": canonical}}, multi=True)
            posts.update({"page_ids": id}, {"$pull": {"page_ids": id}}, multi=True)
    i += 1

