
def import_question(posts, namespaces, upsert, id, title, body, tags, last_activity_date, last_updated_date, score, answers, has_accepted_answer):
    namespaces_for_post = {}
    for name, n in namespaces.items():
        namespace_tags = n.get_tags()
        if not(namespace_tags) or any(map(lambda x: x in tags, namespace_tags)):
            ids = n.get_ids(title, body, tags)
            for a in answers:
                ids = list(set(ids) | set(n.get_ids(title, a["body"], tags)))
            if len(ids) > 0:
                ids = map(lambda x: x.lower(), ids)
                namespaces_for_post[name] = ids

    if len(namespaces_for_post):
        post = {
            "question_id": id,
            "url": "http://stackoverflow.com/questions/%s" % id,
            "namespaces": namespaces_for_post,
            "title": title,
            "score": int(score),
            "answers": len(answers),
            "accepted_answer": has_accepted_answer,
            "last_activity": last_activity_date,
            "last_updated": last_updated_date
        }

        if upsert:
            posts.update({"question_id": id}, post, True)
        else:
            posts.insert(post)

        print "Processed %s question from %s (%s)" % (", ".join(namespaces_for_post.keys()), str(last_activity_date), id)
