import pymongo

connection = pymongo.Connection()
db = connection.stack_doc
posts = db.posts

up_to_date = False

while not up_to_date:
    last_in_database = posts.find_one(sort=[("last_activity", pymongo.DESCENDING)])["last_activity"]
    print "Fetching questions active after " + last_in_database