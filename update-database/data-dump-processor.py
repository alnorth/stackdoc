import dateutil.parser
import pkgutil
from pymongo import Connection
import sys
from xml.sax import make_parser, handler

import stackdoc.languages

languages = []
for importer, modname, ispkg in pkgutil.iter_modules(stackdoc.languages.__path__):
    languages.append(__import__("stackdoc.languages.%s" % modname, fromlist="dummy"))


class SOProcessor(handler.ContentHandler):

    def __init__(self):
        connection = Connection()
        self._db = connection.stackdoc
        self._posts = self._db.posts
        # Get rid of all existing data
        self._posts.remove()

    def startElement(self, name, attrs):
        if name == "row":
            if attrs["PostTypeId"] == "1":
                for l in languages:
                    tags = attrs["Tags"].lstrip("<").rstrip(">").split("><")
                    if any(map(lambda x: x in tags, l.get_tags())):
                        ids = l.get_ids(attrs["Title"], attrs["Body"], tags)

                        if len(ids) > 0:
                            post = {
                                "namespaces": {"dotnet": ids},
                                "question_id": int(attrs["Id"]),
                                "url": "http://stackoverflow.com/questions/%s" % attrs["Id"],
                                "title": attrs["Title"],
                                "score": int(attrs["Score"]),
                                "answers": int(attrs["AnswerCount"]) if "AnswerCount" in attrs else 0,
                                "accepted_answer": "AcceptedAnswerId" in attrs,
                                "last_activity": dateutil.parser.parse(attrs["LastActivityDate"])
                            }
                            self._posts.insert(post)


parser = make_parser()
parser.setContentHandler(SOProcessor())
parser.parse(open(sys.argv[1]))
