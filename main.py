import requests
import cherrypy
import os, os
import json
from threading import Thread
import dbase
from cherrypy.lib import static

botactive = False
url = 'https://api.vk.com/method/users.get?user_id=294940138&v=5.52&access_token=737c6a19d16db39e7dee92e584c64717b125dbc158aebb486c5cec455570a515473c1e3d265c970b1255c'

print(requests.post(url=url).text)

@cherrypy.expose
class GetForm(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, botname, login):
        print(botname)
        result = {'date': dbase.getDate(botname=botname, login=login),
                  'balance': dbase.getBalance(botname=botname, login=login)}
        print(result)
        return result
       # print(json.dumps(result, sort_keys=True))
       # return json.dumps(result, sort_keys=True)

    @cherrypy.tools.accept(media='text/plain')
    def PUT(self, data):
        dbase.updateClient(data=data)

@cherrypy.expose
class GenerateHtml(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return open(file='index.html', encoding='utf8')

@cherrypy.expose
class BotStatus(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, botname, login):
        result = {'date': dbase.getDate(botname=botname, login=login)}
        return result

conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
        },
            # 'tools.response_headers.headers': [('Content-Type', 'application/json')],
        # '/generator': {
        #     'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        #     'tools.response_headers.on': True,
        #     'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        # },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

cherrypy.config.update({'server.socket_host': '127.0.0.1',
                            'server.socket_port': 8080,
                            'tools.sessions.on': True,
                            'engine.autoreload.on': False,
                            'log.access_file': './access.log',
                            'log.error_file': './error.log',
                            })

cherrypy.tree.mount(GenerateHtml(), '/', conf)
cherrypy.tree.mount(GetForm(), '/getForm', conf)
cherrypy.tree.mount(BotStatus(), '/botStatus', conf)


cherrypy.engine.start()
cherrypy.engine.block()


