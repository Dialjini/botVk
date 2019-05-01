import cherrypy
import os, os
import json
import dbase
import price
from cherrypy.lib import static

url = 'test.vkApp.com'

botactive = False
access_token = '737c6a19d16db39e7dee92e584c64717b125dbc158aebb486c5cec455570a515473c1e3d265c970b1255c'
secKey = 'D7UqxfSz3SU8bW5fJmnF'
serviceKey = '88359d2a88359d2a88359d2a5f885c21918883588359d2ad492dab541f7422bd024a392'


# print(requests.post(url=url).text)

def getCount(balance):
    result = 0
    while (True):
        if ((int(balance) - price.price['year']) >= 0):
            balance = balance - price.price['year']
            result = result + 365
            continue
        if ((int(balance) - price.price['3_months']) >= 0):
            balance = balance - price.price['3_months']
            result = result + 90
            continue
        if ((int(balance) - price.price['month']) >= 0):
            balance = balance - price.price['month']
            result = result + 30
            continue
        break
    return result


class user():
    login = ''
    botname = ''


@cherrypy.expose
class GetForm(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **data):
        print(data)
        login = user.login
        botname = user.botname
        print(botname)
        print(login)
        date = dbase.getDate(botname=botname, login=login)
        balance = dbase.getBalance(botname=botname, login=login)
        result = {'date': date, 'balance': balance,
                  'count': getCount(balance)}

        print(json.dumps(result, sort_keys=True))
        return json.dumps(result, sort_keys=True)


@cherrypy.expose
class UpdateClient(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, crm, lkcrm, apikey, **data):
        print(data)
        botname = user.botname
        login = user.login
        dbase.updateClient(botname=botname, login=login, crm=crm, lkcrm=lkcrm, apikey=apikey)


@cherrypy.expose
class GenerateHtml(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **data):
        if (data != {'login': 'test', 'botname': 'test'}):
            user.login = data['user_id']
            user.botname = data['api_id']
            return open(file='index.html', encoding='utf8')

        else:
            print(data)
            print('login = ' + user.login)
            print('botname = ' + user.botname)
            return json.dumps({'login': user.login, 'botname': user.botname}, sort_keys=True)


@cherrypy.expose
class BotStatus(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **data):
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
