import re
import sys
from pymongo import Connection

if len(sys.argv) < 2:
    print "This script expects one argument: A URL prefix to search for."
else:
    # Set up the database connection
    connection = Connection()
    stackdb = connection.stackdb

    start_with = sys.argv[1]

    for q in stackdb.questions.find():
        body = q["body"]
        if start_with in body:
            matches = re.findall(r'<a href="([^"]+)"', body)
            for url in filter(lambda x: x.startswith(start_with), matches):
                print url, "-", (", ".join(q["tags"]))
