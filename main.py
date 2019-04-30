import requests
import cherrypy
import os, os
import json
from threading import Thread
import dbase
from cherrypy.lib import static


url = 'test.vkApp.com'

botactive = False
url = 'https://api.vk.com/method/users.get?user_id=294940138&v=5.52&access_token=737c6a19d16db39e7dee92e584c64717b125dbc158aebb486c5cec455570a515473c1e3d265c970b1255c'
secKey = 'D7UqxfSz3SU8bW5fJmnF'
serviceKey = '88359d2a88359d2a88359d2a5f885c21918883588359d2ad492dab541f7422bd024a392'

# print(requests.post(url=url).text)

@cherrypy.expose
class GetForm(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, botname, login):
        print(botname)
        result = {'date': dbase.getDate(botname=botname, login=login),
                  'balance': dbase.getBalance(botname=botname, login=login)}

        print(json.dumps(result, sort_keys=True))
        return json.dumps(result, sort_keys=True)

@cherrypy.expose
class UpdateClient(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, botname, login, crm, lkcrm, apikey):
        dbase.updateClient(botname=botname, login=login, crm=crm, lkcrm=lkcrm, apikey=apikey)


class GenerateHtml(object):
    @cherrypy.expose
    def index(self, **data):
        print('som body get')
        print(data['access_token'])
        return open(file='index.html', encoding='utf8')

@cherrypy.expose
class BotStatus(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, botname, login, mode):
        return 'OK'



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
                            'server.socket_port': 443,
                            'tools.sessions.on': True,
                            'engine.autoreload.on': False,
                            'log.access_file': './access.log',
                            'log.error_file': './error.log',
                            'server.ssl_module': 'builtin',
                            'server.ssl_certificate': 'cert.pem',
                            'server.ssl_private_key': 'privkey.pem'
                            })

cherrypy.tree.mount(GenerateHtml(), '/', conf)
cherrypy.tree.mount(GetForm(), '/getForm', conf)
cherrypy.tree.mount(BotStatus(), '/botStatus', conf)
cherrypy.tree.mount(UpdateClient(), '/updateClient', conf)


cherrypy.engine.start()
cherrypy.engine.block()


