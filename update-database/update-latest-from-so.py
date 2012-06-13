import pymongo
import stackexchange
import re
import time

so = stackexchange.Site(stackexchange.StackOverflow)

so.be_inclusive()

connection = pymongo.Connection()
db = connection.stack_doc
posts = db.posts

last_in_database = posts.find_one(sort=[("last_activity", pymongo.DESCENDING)])["last_activity"]
last_in_database_as_unix = int(time.mktime(last_in_database.timetuple()))
print "Fetching questions active after %s" % str(last_in_database)
rq = so.recent_questions(min=last_in_database_as_unix, order="asc")
for q in rq:
    if (".net" in q.tags or "c#" in q.tags or "vb.net" in q.tags or "f#" in q.tags) and "http://msdn.microsoft.com/en-us/library/" in q.body:
        matches = re.findall(r"http://msdn\.microsoft\.com/en\-us/library/([a-zA-Z0-9\.]+?)(_[a-z]+)?(\(v=vs\.\d+\))?(\.aspx)?(?:$|[^a-zA-z0-9._])", q.body)
        ids = []
        for match_tuple in matches:
            ids.append(match_tuple[0])
        if len(ids) > 0:
            post = posts.find_one({"question_id": q.id})
            previously_existed = False
            if post:
                previously_existed = True
            else:
                post = {}

            post["page_ids"] = ids
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

            print "Inserted/updated question from %s " % str(q.last_activity_date)
    time.sleep(0.05) # Do our own throttling as the built in throttling seems broken
