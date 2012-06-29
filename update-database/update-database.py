import pkgutil
from pymongo import Connection

from stackdoc.questionimport import import_question
import stackdoc.languages

# Set up the database connection
connection = Connection()
db = connection.stackdoc
posts = db.posts
language_records = db.languages

# Load the list of languages
languages = []
for importer, modname, ispkg in pkgutil.iter_modules(stackdoc.languages.__path__):
    languages.append(__import__("stackdoc.languages.%s" % modname, fromlist="dummy"))

# Check if any versions are different from the saved versions
version_outdated = False
for l in languages:
    record = language_records.find_one({"name": l.get_name()})
    if record:
        if record.version != l.get_version():
            print "Namespace %s outdated (%s != %s), will import posts.xml" % (l.get_name(), record.version, l.get_version())
            version_outdated = True
    else:
        print "Namespace %s is new, will import posts.xml" % l.get_name()
        version_outdated = True

# If so then process the posts.xml file

# Set the version for all languages and last activity date for any language missing it

# Load SO questions from the earliest last activity date

# Every 100 questions set the last activity date for all languages to at least that in the current question
