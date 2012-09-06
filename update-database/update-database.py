import logging
import logging.config
import pkgutil
import pymongo
import sys
import time
from xml.sax import make_parser, handler

from stackdoc.questionimport import import_question
import stackdoc.namespaces

####### Variables
# The minimum score required for a question to be processed
minimum_question_score = 2
# The minimum score required for an answer to be processed
minimum_answer_score = minimum_question_score

# Set up the database connection
connection = pymongo.Connection()
db = connection.stackdoc
stackdb = connection.stackdb
posts = db.posts
namespace_records = db.namespaces

logging.config.fileConfig("logging.conf")


# Load the list of namespaces
namespaces = {}
for importer, modname, ispkg in pkgutil.iter_modules(stackdoc.namespaces.__path__):
    namespaces[modname] = __import__("stackdoc.namespaces.%s" % modname, fromlist="dummy")


# Check if any versions are different from the saved versions
version_outdated = False
for name, n in namespaces.items():
    record = namespace_records.find_one({"name": name})
    if record:
        if record["version"] != n.get_version():
            logging.info("Namespace %s outdated (%s != %s), will import whole collection" % (name, record["version"], n.get_version()))
            version_outdated = True
    else:
        logging.info("Namespace %s is new, will import whole collection" % name)
        version_outdated = True

def import_all_questions(collection, namespaces, questions, upsert):
    for q in questions:
        if q["score"] >= minimum_question_score:
            import_question(
                collection,
                namespaces,
                upsert,
                minimum_answer_score,
                q["question_id"],
                q["title"],
                q["body"],
                q["tags"],
                q["last_activity_date"],
                q["last_updated_date"],
                q["score"],
                q["answers"],
                "accepted_answer_id" in q and q["accepted_answer_id"] > 0
            )


# If so then process the whole collection
if version_outdated:
    tmp_posts = db.tmp_posts
    tmp_posts.drop()

    # We don't care about ordering here because we're updating the whole collection in one go
    import_all_questions(tmp_posts, namespaces, stackdb.questions.find(), False)

    # Make sure the correct indexes are in place
    tmp_posts.ensure_index("question_id", unique=True)
    tmp_posts.ensure_index("last_updated")
    for name, n in namespaces.items():
        tmp_posts.ensure_index("namespaces.%s" % name)

    posts.drop()
    tmp_posts.rename("posts")
    posts = db.posts

    # Set the version for all namespaces
    for name, n in namespaces.items():
        namespace_records.update(
            {"name": name},
            {"name": name, "version": n.get_version()},
            upsert=True
        )

else:
    # We've previously imported most of the questions, we now just need to catch up with what's changed since.
    latest_updated_question = posts.find_one(sort=[("last_updated", pymongo.DESCENDING)])
    last_updated_date = latest_updated_question["last_updated"]

    stackdb.questions.ensure_index([("last_updated_date", pymongo.ASCENDING)])

    logging.info("Processing questions updated after %s" % str(last_updated_date))
    sorted_questions = stackdb.questions.find({"last_updated_date": {"$gt": last_updated_date}}, sort=[("last_updated_date", pymongo.ASCENDING)])
    import_all_questions(posts, namespaces, sorted_questions, True)
