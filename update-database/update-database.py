import dateutil.parser
import pkgutil
from pymongo import Connection
import stackexchange
import sys
import time
from xml.sax import make_parser, handler

from stackdoc.questionimport import import_question
import stackdoc.languages


# Set up the database connection
connection = Connection()
db = connection.stackdoc
posts = db.posts
language_records = db.languages
settings = db.settings


# Load the list of languages
languages = []
for importer, modname, ispkg in pkgutil.iter_modules(stackdoc.languages.__path__):
    languages.append(__import__("stackdoc.languages.%s" % modname, fromlist="dummy"))


# Make sure the correct indexes are in place
posts.ensure_index("question_id", unique=True)
for l in languages:
    posts.ensure_index("namespaces.%s" % l.get_name())


# Check if any versions are different from the saved versions
version_outdated = False
for l in languages:
    record = language_records.find_one({"name": l.get_name()})
    if record:
        if record["version"] != l.get_version():
            print "Namespace %s outdated (%s != %s), will import posts.xml" % (l.get_name(), record["version"], l.get_version())
            version_outdated = True
    else:
        print "Namespace %s is new, will import posts.xml" % l.get_name()
        version_outdated = True


# If so then process the posts.xml file
if version_outdated:
    latest_imported_activity = None
    class SOProcessor(handler.ContentHandler):

        def startElement(self, name, attrs):
            if name == "row":
                if attrs["PostTypeId"] == "1":
                    global latest_imported_activity
                    global posts
                    last_activity_date = dateutil.parser.parse(attrs["LastActivityDate"])
                    if not latest_imported_activity or latest_imported_activity < last_activity_date:
                        latest_imported_activity = last_activity_date
                    import_question(
                        posts,
                        languages,
                        int(attrs["Id"]),
                        attrs["Title"],
                        attrs["Body"],
                        attrs["Tags"].lstrip("<").rstrip(">").split("><"),
                        last_activity_date,
                        int(attrs["Score"]),
                        int(attrs["AnswerCount"]) if "AnswerCount" in attrs else 0,
                        "AcceptedAnswerId" in attrs
                    )

    parser = make_parser()
    parser.setContentHandler(SOProcessor())
    parser.parse(open(sys.argv[1]))

    # Set the version for all languages and last activity date
    for l in languages:
        language_records.update(
            {"name": l.get_name()},
            {"name": l.get_name(), "version": l.get_version()},
            upsert=True
        )
    settings.update(
        {"key": "latest_activity_date"},
        {"key": "latest_activity_date", "value": latest_imported_activity},
        upsert=True
    )


# Load SO questions from the earliest last activity date
so = stackexchange.Site(stackexchange.StackOverflow)
so.be_inclusive()
so.impose_throttling = True

latest_activity_date = settings.find_one({"key": "latest_activity_date"})["value"]
latest_activity_date_as_unix = int(time.mktime(latest_activity_date.timetuple()))
print "Fetching questions active after %s" % str(latest_activity_date)
rq = so.recent_questions(min=latest_activity_date_as_unix, order="asc")
index = 0
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

    # Every 100 questions set the last activity date
    index += 1
    if index % 100 == 0:
        settings.update(
            {"key": "latest_activity_date"},
            {"key": "latest_activity_date", "value": q.last_activity_date},
            upsert=True
        )

