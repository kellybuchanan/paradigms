# Kelly Buchanan
# kbuchana
# Timothy Gallagher
# tgallag6

import cherrypy
from moviesController import MovieController
from resetController import ResetController
from ratingsController import RatingsController
from movies_library import _movie_database

class optionsController:
    def OPTIONS(self, *args, **kwargs):
        return ""

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

def start_service():
    dispatcher = cherrypy.dispatch.RoutesDispatcher()


    mdb = _movie_database()

    movieController     = MovieController(mdb=mdb)
    resetController     = ResetController(mdb=mdb)
    ratingsController   = RatingsController(mdb=mdb)

    dispatcher.connect('movie_get', '/movies/:movie_id', controller=movieController, action = 'GET_KEY', conditions=dict(method=['GET']))
    dispatcher.connect('movie_put', '/movies/:movie_id', controller=movieController, action = 'PUT_KEY', conditions=dict(method=['PUT']))
    dispatcher.connect('movie_delete', '/movies/:movie_id', controller=movieController, action = 'DELETE_KEY', conditions=dict(method=['DELETE']))
    dispatcher.connect('movie_index_get', '/movies/', controller=movieController, action = 'GET_INDEX', conditions=dict(method=['GET']))
    dispatcher.connect('movie_index_post', '/movies/', controller=movieController, action = 'POST_INDEX', conditions=dict(method=['POST']))
    dispatcher.connect('movie_index_delete', '/movies/', controller=movieController, action = 'DELETE_INDEX', conditions=dict(method=['DELETE']))

    dispatcher.connect('reset_put', '/reset/:movie_id', controller=resetController, action = 'PUT_KEY', conditions=dict(method=['PUT']))
    dispatcher.connect('reset_index_put', '/reset/', controller=resetController, action = 'PUT_INDEX', conditions=dict(method=['PUT']))

    dispatcher.connect('rating_get', '/ratings/:movie_id', controller=ratingsController, action = 'GET_KEY', conditions=dict(method=['GET']))


    # CORS related options connections
    dispatcher.connect('movie_key_options', '/movies/:movie_id', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('movie_options', '/movies/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('reset_key_options', '/reset/:movie_id', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('reset_options', '/reset/', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('rating_options', '/ratings/:movie_id', controller=optionsController, action = 'OPTIONS', conditions=dict(method=['OPTIONS']))



    conf = {
	'global': {
        'server.thread_pool': 5,
	    'server.socket_host': 'student10.cse.nd.edu',
	    'server.socket_port': 51091,
	    },
	'/': {
	    'request.dispatch': dispatcher,
            'tools.CORS.on':True,
	    }
    }

    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)

# end of start_service


if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    start_service()
