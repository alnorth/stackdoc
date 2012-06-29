import dateutil.parser
import pkgutil
from pymongo import Connection
import sys
from xml.sax import make_parser, handler

from stackdoc.questionimport import import_question
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
        #self._posts.remove()

    def startElement(self, name, attrs):
        if name == "row":
            if attrs["PostTypeId"] == "1":
                import_question(
                    self._posts,
                    languages,
                    int(attrs["Id"]),
                    attrs["Title"],
                    attrs["Body"],
                    attrs["Tags"].lstrip("<").rstrip(">").split("><"),
                    dateutil.parser.parse(attrs["LastActivityDate"]),
                    int(attrs["Score"]),
                    int(attrs["AnswerCount"]) if "AnswerCount" in attrs else 0,
                    "AcceptedAnswerId" in attrs
                )

parser = make_parser()
parser.setContentHandler(SOProcessor())
parser.parse(open(sys.argv[1]))
