import pymongo
import stackexchange
import time

so = stackexchange.Site(stackexchange.StackOverflow, "WNe2LOp*hdsbD5U7kp0bhg((")

so.be_inclusive()

connection = pymongo.Connection()
db = connection.stack_doc
posts = db.posts

up_to_date = False

while not up_to_date:
    last_in_database = posts.find_one(sort=[("last_activity", pymongo.DESCENDING)])["last_activity"]
    last_in_database_as_unix = int(time.mktime(last_in_database.timetuple()))
    print "Fetching questions active after %s" % last_in_database_as_unix
    rq = so.recent_questions(from_date=last_in_database_as_unix)
    print rq[0]
