
def import_question(posts, languages, id, title, body, tags, last_activity_date, score, answer_count, has_accepted_answer):
    namespaces = {}
    for l in languages:
        if any(map(lambda x: x in tags, l.get_tags())):
            ids = l.get_ids(title, body, tags)
            if len(ids) > 0:
                ids = map(lambda x: x.lower(), ids)
                namespaces[l.get_name()] = ids

    if len(namespaces):
        post = posts.find_one({"question_id": int(id)})
        previously_existed = False
        if post:
            previously_existed = True
        else:
            post = {}

        post["namespaces"] = namespaces
        post["question_id"] = int(id)
        post["url"] = "http://stackoverflow.com/questions/%s" % id
        post["title"] = title
        post["score"] = int(score)
        post["answers"] = int(answer_count)
        post["accepted_answer"] = has_accepted_answer
        post["last_activity"] = last_activity_date

        if previously_existed:
            posts.update({"question_id": int(id)}, post)
        else:
            posts.insert(post)

        print "%s %s question from %s (%s)" % ("Updated" if previously_existed else "Inserted", ", ".join(namespaces.keys()), str(last_activity_date), id)
