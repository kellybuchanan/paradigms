# Kelly Buchanan
# kbuchana
# Timothy Gallagher
# tgallag6

import cherrypy
import re, json
from movies_library import _movie_database

class MovieController(object):

        def __init__(self, mdb=None):
                if mdb is None:
                    self.mdb = _movie_database()
                else:
                    self.mdb = mdb

                self.mdb.load_movies('movies.dat')

        def GET_KEY(self, movie_id):
                output = {'result':'success'}
                movie_id = int(movie_id)


                try:
                    movie = self.mdb.get_movie(movie_id)
                    if movie is not None:
                        output['id'] = movie_id
                        output['title'] = movie[0]
                        output['genres'] = movie[1]
                    else:
                        output['result'] = 'error'
                        output['message'] = 'movie not found'
                except Exception as ex:
                    output['result'] = 'error'
                    output['message'] = str(ex)

                return json.dumps(output)

        def PUT_KEY(self, movie_id):
                output = {'result':'success'}
                movie_id = int(movie_id)

                data = json.loads(cherrypy.request.body.read().decode('utf-8'))

                movie = list()
                movie.append(data['title'])
                movie.append(data['genres'])

                self.mdb.set_movie(movie_id, movie)

                return json.dumps(output)

        def DELETE_KEY(self, movie_id):
                output = {'result' : 'success'}
                movie_id = int(movie_id)

                try:
                    self.mdb.delete_movie(movie_id)
                except Exception as ex:
                    output['result'] = 'error'
                    output['message'] = str(ex)

                return json.dumps(output)

        def GET_INDEX(self):
                output = {'result':'success'}
                output['movies'] = []

                try:
                    for mid in self.mdb.get_movies():
                        movie = self.mdb.get_movie(mid)
                        dmovie = {'id':mid, 'title':movie[0], 'genres':movie[1]}
                        output['movies'].append(dmovie)
                except Exception as ex:
                    output['result'] = 'error'
                    output['message'] = str(ex)

                return json.dumps(output)

        def POST_INDEX(self):
                output = {'result': 'success'}
                data = json.loads(cherrypy.request.body.read())
                movie = list()
                
                maxx = max(self.mdb.get_movies()) + 1
                output['id'] = maxx  

                try:
                    movie.append(data['title'])
                    movie.append(data['genres'])
                    self.mdb.set_movie(maxx, movie)
                except Exception as ex:
                    output['result']    = 'error'
                    output['message']   = str(ex)

                return json.dumps(output)
 
        def DELETE_INDEX(self):
                output = {'result' : 'success'}

                try: 
                    for mid in list(self.mdb.get_movies()):
                        self.mdb.delete_movie(mid)
                   
                except Exception as ex:
                    output['result']    = 'error'
                    output['message']   = str(ex)

                return json.dumps(output)
                
