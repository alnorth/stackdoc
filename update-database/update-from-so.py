import pkgutil
import pymongo
import stackexchange
import re
import time
import urllib

import stackdoc.languages

languages = []
for importer, modname, ispkg in pkgutil.iter_modules(stackdoc.languages.__path__):
    languages.append(__import__("stackdoc.languages.%s" % modname, fromlist="dummy"))

def is_msdn_id(string):
    return bool(re.match("^[a-zA-Z0-9]{8}$", string))

def map_msdn_id(msdn_id):
    if is_msdn_id(msdn_id):
        handle = urllib.urlopen("http://msdnid.alnorth.com/" + msdn_id)
        if handle.getcode() == 200:
            canonical = handle.readline()
            return canonical

so = stackexchange.Site(stackexchange.StackOverflow)

so.be_inclusive()
so.impose_throttling = True

connection = pymongo.Connection()
db = connection.stackdoc
posts = db.posts

last_in_database = posts.find_one(sort=[("last_activity", pymongo.DESCENDING)])["last_activity"]
last_in_database_as_unix = int(time.mktime(last_in_database.timetuple()))
print "Fetching questions active after %s" % str(last_in_database)
rq = so.recent_questions(min=last_in_database_as_unix, order="asc")
for q in rq:
    namespaces = {}
    for l in languages:
        if any(map(lambda x: x in q.tags, l.get_tags())):
            ids = l.get_ids(q.title, q.body, q.tags)
            if len(ids) > 0:
                ids = map(lambda x: x.lower(), ids)
                namespaces[l.get_name()] = ids

    if len(namespaces):
        post = posts.find_one({"question_id": q.id})
        previously_existed = False
        if post:
            previously_existed = True
        else:
            post = {}

        post["namespaces"] = namespaces
        post["question_id"] = int(q.id)
        post["url"] = "http://stackoverflow.com/questions/%s" % q.id
        post["title"] = q.title
        post["score"] = int(q.score)
        post["answers"] = int(q.answer_count)
        post["accepted_answer"] = hasattr(q, "accepted_answer_id")
        post["last_activity"] = q.last_activity_date

        if previously_existed:
            posts.update({"question_id": q.id}, post)
        else:
            posts.insert(post)

        print "%s %s question from %s (%s)" % ("Updated" if previously_existed else "Inserted", ", ".join(namespaces.keys()), str(q.last_activity_date), q.id)
