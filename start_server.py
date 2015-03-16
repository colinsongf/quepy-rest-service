import web
import quepy
urls = (
    '/dbpedia', 'queryDbpedia',
    '/freebase', 'queryFreebase',
    '/', 'pathParam'
)


class pathParam:
    def GET(self):
        query_string = web.input()
        type = query_string.type
        if type == 'sparql':
            dbpedia = quepy.install("dbpedia")
            target, query, metadata = dbpedia.get_query(query_string.q)
            return query
        elif type == 'mql':
            freebase = quepy.install("freebase")
            target, query, metadata = freebase.get_query(query_string.q)
            return query
        else:
            return ""


class queryDbpedia:
    def GET(self):
        query_string = web.input()
        dbpedia = quepy.install("dbpedia")
        target, query, metadata = dbpedia.get_query(query_string.q)
        return query


class queryFreebase:
    def GET(self):
        query_string = web.input()
        freebase = quepy.install("freebase")
        target, query, metadata = freebase.get_query(query_string.q)
        return query

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    #  dbpedia = quepy.install("dbpedia")
    #  target, query, metadata = dbpedia.get_query("Where is Albert Einstein from?")
    #  print(query)
