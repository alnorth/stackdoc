import pkgutil
import pymongo
import stackexchange
import re
import time
import urllib

from stackdoc.questionimport import import_question
import stackdoc.languages

languages = []
for importer, modname, ispkg in pkgutil.iter_modules(stackdoc.languages.__path__):
    languages.append(__import__("stackdoc.languages.%s" % modname, fromlist="dummy"))

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
    import_question(
        posts,
        languages,
        int(q.id),
        q.title,
        q.body,
        q.tags,
        q.last_activity_date,
        int(q.score),
        int(q.answer_count),
        hasattr(q, "accepted_answer_id")
    )
