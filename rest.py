import web
import quepy

urls = (
  '/dbpedia', 'queryDbpedia',
  '/freebase', 'queryFreebase',
)

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
