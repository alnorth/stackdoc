import sys

from xml.sax import make_parser, handler

class SOProcessor(handler.ContentHandler):

    def __init__(self):
        self._count = 0

    def startElement(self, name, attrs):
        if name == "row":
            if attrs["PostTypeId"] == "1":
                if "<.net>" in attrs["Tags"] and "http://msdn.microsoft.com/" in attrs["Body"]:
                    self._count += 1
                    print self._count
            
parser = make_parser()
parser.setContentHandler(SOProcessor())
parser.parse(open(sys.argv[1]))