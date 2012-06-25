import dateutil.parser
from pymongo import Connection
import re
import sys
import urllib
from xml.sax import make_parser, handler

def is_msdn_id(string):
    return bool(re.match("^[a-zA-Z0-9]{8}$", string))

def map_msdn_id(msdn_id):
    if is_msdn_id(msdn_id):
        handle = urllib.urlopen("http://msdnid.alnorth.com/" + msdn_id)
        if handle.getcode() == 200:
            canonical = handle.readline()
            return canonical

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
                        match_id = match_tuple[0]
                        ids.append(match_id)
                        mapped_id = map_msdn_id(match_id)
                        if mapped_id:
                            print "%s - %s (mapped)" % (attrs["Id"], mapped_id)
                            ids.append(mapped_id)
                        print "%s - %s" % (attrs["Id"], match_id)
                    if len(ids) > 0:
                        post = {
                            "page_ids": {"dotnet": ids},
                            "question_id": int(attrs["Id"]),
                            "url": "http://stackoverflow.com/questions/%s" % attrs["Id"],
                            "title": attrs["Title"],
                            "score": int(attrs["Score"]),
                            "answers": int(attrs["AnswerCount"]) if "AnswerCount" in attrs else 0,
                            "accepted_answer": "AcceptedAnswerId" in attrs,
                            "last_activity": dateutil.parser.parse(attrs["LastActivityDate"])
                        }
                        self._posts.insert(post)
                    else:
                        print "**** %s - Contains URL prefix, but with no regex matches ****" % attrs["Id"]

parser = make_parser()
parser.setContentHandler(SOProcessor())
parser.parse(open(sys.argv[1]))
