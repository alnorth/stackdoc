import re
import sys
from xml.sax import make_parser, handler

if len(sys.argv) < 3:
    print "This script expects two arguments: \n1. The path to a posts.xml file from a Stack Overflow data dump.\n2. A URL prefix to search for."
else:
    start_with = sys.argv[2]

    class SOProcessor(handler.ContentHandler):

        def startElement(self, name, attrs):
            if name == "row":
                if attrs["PostTypeId"] == "1":
                    body = attrs["Body"]
                    if start_with in body:
                        matches = re.findall(r'<a href="([^"]+)"', body)
                        for url in filter(lambda x: x.startswith(start_with), matches):
                            print url, attrs["Tags"]

    parser = make_parser()
    parser.setContentHandler(SOProcessor())
    parser.parse(open(sys.argv[1]))
