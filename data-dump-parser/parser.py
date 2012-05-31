import dateutil.parser
from pymongo import Connection
import re
import sys
from xml.sax import make_parser, handler

class SOProcessor(handler.ContentHandler):

    def __init__(self):
        connection = Connection()
        self._db = connection.stack_doc
        self._posts = self._db.posts
        # Get rid of all existing data
        self._posts.remove()

    def startElement(self, name, attrs):
        if name == "row":
            if attrs["PostTypeId"] == "1":
                if ("<.net>" in attrs["Tags"] or "<c#>" in attrs["Tags"] or "<vb.net>" in attrs["Tags"] or "<asp.net>" in attrs["Tags"] or "<f#>" in attrs["Tags"]) and "http://msdn.microsoft.com/en-us/library/" in attrs["Body"]:
                    matches = re.findall(r"http://msdn\.microsoft\.com/en\-us/library/([a-zA-Z0-9\.]+?)(_[a-z]+)?(\(v=vs\.\d+\))?(\.aspx)?(?:$|[^a-zA-z0-9._])", attrs["Body"])
                    ids = []
                    for match_tuple in matches:
                        ids.append(match_tuple[0])
                        print "%s - %s" % (attrs["Id"], match_tuple[0])
                    if len(ids) > 0:
                        post = {
                            "page_ids": ids,
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
