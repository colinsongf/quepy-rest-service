import web
from Model import ReturnModel
import quepy
import demjson

urls = (
    '/dbpedia', 'QueryDbpedia',
    '/freebase', 'QueryFreebase',
    '/', 'PathParam'
)


class PathParam:
    def GET(self):
        query_string = web.input()
        query_type = query_string.type
        return_model = ReturnModel("", None)
        if query_type == 'sparql':
            dbpedia = quepy.install("dbpedia")
            return_model = dbpedia.get_query(query_string.q)

        elif query_type == 'mql':
            freebase = quepy.install("freebase")
            return_model = freebase.get_query(query_string.q)

        web.header('Content-Type', 'application/json')
        return demjson.encode(return_model.toJSON())


class QueryDbpedia:
    def GET(self):
        query_string = web.input()
        dbpedia = quepy.install("dbpedia")
        return_model = dbpedia.get_query(query_string.q)

        web.header('Content-Type', 'application/json')
        return demjson.encode(return_model.toJSON())


class QueryFreebase:
    def GET(self):
        query_string = web.input()
        freebase = quepy.install("freebase")

        return_model = freebase.get_query(query_string.q)
        return demjson.encode(return_model.toJSON())


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()