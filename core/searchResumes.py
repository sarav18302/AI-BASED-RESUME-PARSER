
def search_resumes(query,db):
    query_list = query.split()
    # for q in query_list:
    #     db.collection.find({$text: {$search: "elasticsearch"}}, {score: {$meta: "textScore"}}).sort({score: {$meta: "textScore"}})