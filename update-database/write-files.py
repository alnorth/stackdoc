import json
import os
from pymongo import Connection
import shutil

connection = Connection()
db = connection.stackdoc
posts = db.posts

shutil.rmtree("dotnet", True)
os.makedirs("dotnet")

for id in posts.distinct("page_ids"):
	questions = []
	for q in posts.find({"page_ids": id}):
		questions.append({
			"id": q["question_id"],
			"url": q["url"],
			"title": q["title"],
			"score": q["score"],
			"answers": q["answers"],
			"accepted_answer": q["accepted_answer"]
		})
	f = open("dotnet/%s.json" % id, "w")
	f.write(json.dumps(questions))
	f.close()
	print id
