
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
        update = True
        if post:
            previously_existed = True
            # Only update title, score etc. if this is the latest data
            update = post["last_activity"] < last_activity_date
        else:
            post = {
                "question_id": int(id),
                "url": "http://stackoverflow.com/questions/%s" % id
            }

        post["namespaces"] = namespaces
        if update:
            post["title"] = title
            post["score"] = int(score)
            post["answers"] = int(answer_count)
            post["accepted_answer"] = has_accepted_answer
            post["last_activity"] = last_activity_date

        if previously_existed:
            posts.update({"question_id": int(id)}, post)
        else:
            posts.insert(post)

        update_text = "Fully updated" if update else "Partially updated"
        print "%s %s question from %s (%s)" % (update_text if previously_existed else "Inserted", ", ".join(namespaces.keys()), str(last_activity_date), id)
