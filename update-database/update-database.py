import dateutil.parser
import pkgutil
from pymongo import Connection
import stackexchange
import sys
import time
from xml.sax import make_parser, handler

from stackdoc.questionimport import import_question
import stackdoc.namespaces


# Set up the database connection
connection = Connection()
db = connection.stackdoc
stackdb = connection.stackdb
posts = db.posts
namespace_records = db.namespaces
settings = db.settings


# Load the list of namespaces
namespaces = {}
for importer, modname, ispkg in pkgutil.iter_modules(stackdoc.namespaces.__path__):
    namespaces[modname] = __import__("stackdoc.namespaces.%s" % modname, fromlist="dummy")


# Make sure the correct indexes are in place
posts.ensure_index("question_id", unique=True)
for name, n in namespaces.items():
    posts.ensure_index("namespaces.%s" % name)


# Check if any versions are different from the saved versions
version_outdated = False
for name, n in namespaces.items():
    record = namespace_records.find_one({"name": name})
    if record:
        if record["version"] != n.get_version():
            print "Namespace %s outdated (%s != %s), will import whole collection" % (name, record["version"], n.get_version())
            version_outdated = True
    else:
        print "Namespace %s is new, will import whole collection" % name
        version_outdated = True


# If so then process the whole collection
if version_outdated:
    tmp_posts = db.tmp_posts
    tmp_posts.drop()

    for q in stackdb.questions.find():
        import_question(
            tmp_posts,
            namespaces,
            q["question_id"],
            q["title"],
            q["body"],
            q["tags"],
            q["last_activity_date"],
            q["score"],
            len(q["answers"]),
            q["accepted_answer_id"] > 0
        )

    # Set the version for all namespaces and last activity date
    for name, n in namespaces.items():
        namespace_records.update(
            {"name": name},
            {"name": name, "version": n.get_version()},
            upsert=True
        )



# Load SO questions from the earliest last activity date
so = stackexchange.Site(stackexchange.StackOverflow)
so.be_inclusive()
so.impose_throttling = True

latest_activity_date = settings.find_one({"key": "latest_activity_date"})["value"]
latest_activity_date_as_unix = int(time.mktime(latest_activity_date.timetuple()))
print "Fetching questions active after %s" % str(latest_activity_date)
rq = so.recent_questions(min=latest_activity_date_as_unix, order="asc", answers="false", pagesize=100)
index = 0
requests_left_current = 0
for q in rq:
    import_question(
        posts,
        namespaces,
        int(q.id),
        q.title,
        q.body,
        q.tags,
        q.last_activity_date,
        int(q.score),
        int(q.answer_count),
        hasattr(q, "accepted_answer_id")
    )

    # Every 20 questions set the last activity date
    index += 1
    if index % 20 == 0:
        settings.update(
            {"key": "latest_activity_date"},
            {"key": "latest_activity_date", "value": q.last_activity_date},
            upsert=True
        )

    # Monitor our request allowance. Pause if we're running out
    if (requests_left_current != so.requests_left) and so.requests_left < 100:
        print "%s requests left, pausing" % so.requests_left
        requests_left_current = so.requests_left
        time.sleep(60)
