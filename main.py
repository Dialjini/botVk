import cherrypy
import os, os
import json
import dbase
import price
from threading import Thread
from cherrypy.lib import static

url = '31.31.201.218:8050'

# -------------------------------------------------<Threading>----------------------------------------------------------

botactive = 'off'
active_clients = []

def botWork(login):
    return 'OK'

def closeThread(login):
    for i in active_clients:
        if login == i['login']:
            active_clients.remove(i)
            break

def upBot(login, status):
    if status == 'on':
        active_clients.append({'login': login, 'thread': Thread(target=botWork, args=(login, ))})

    if status == 'off':
        closeThread(login)

for i in dbase.getActiveUsers():
    active_clients.append({'login': i[0], 'thread': Thread(target=botWork, args=(i[0], ))})

# --------------------------------------------------<Functions>---------------------------------------------------------

def reloadSubscribe(login):
    if(dbase.getBalance(login) >= 18490):
        dbase.updateRate(login, '1 год.')
        dbase.updateBalance(login, -18490)
        return True
    if(dbase.getBalance(login) >= 4990):
        dbase.updateRate(login, '3 месяца.')
        dbase.updateBalance(login, -4990)
        return True
    if(dbase.getBalance(login) >= 2490):
        dbase.updateRate(login, '1 месяц.')
        dbase.updateBalance(login, -2490)
        return True
    return False


def getCount(balance):
    result = 0
    balance = int(balance)
    while (True):
        if ((balance - price.price['year']) >= 0):
            balance = balance - price.price['year']
            result = result + 365
            continue
        if ((balance - price.price['3_months']) >= 0):
            balance = balance - price.price['3_months']
            result = result + 90
            continue
        if ((balance - price.price['month']) >= 0):
            balance = balance - price.price['month']
            result = result + 30
            continue
        break
    return result

# -------------------------------------------------<Server>-------------------------------------------------------------

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
        date = dbase.getDate(login=login)
        if(dbase.getLimit(login) == -1):
            check = reloadSubscribe(login)
            if not check:
                date = date + ', Бот отключён. Чтобы восстановить работу бота - пополните баланс'
        balance = dbase.getBalance(login=login)
        result = {'date': date, 'balance': balance,
                  'count': getCount(balance), 'crm': dbase.getFields(login)[0], 'lkcrm': dbase.getFields(login)[1],
                  'apikey': dbase.getFields(login)[2], 'rate': dbase.getRate(login)}

        print(json.dumps(result, sort_keys=True))
        return json.dumps(result, sort_keys=True)


@cherrypy.expose
class UpdateClient(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **data):
        print('here ' + str(data))
        botname = user.botname
        login = user.login
        print(dbase.clientIsNew(login))
        if(dbase.clientIsNew(login)):
            print('login is ' + login)
            if(dbase.getToday()['flag'] == '+'):
                date = dbase.getToday()['result'] + 1000000
            else:
                date = dbase.getToday()['result'] - 12000000
            dbase.addClient(botname=botname, login=login, crm=data['crm'], date=date, apikey=data['apikey'],
                            email='0', lkcrm=data['lkcrm'], password='', rate='1 месяц')
        else:
            dbase.updateClient(botname=botname, login=login, crm=data['crm'], lkcrm=data['lkcrm'], apikey=data['apikey'])


@cherrypy.expose
class GenerateHtml(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **data):
        if (data != {'login': 'test', 'botname': 'test'}):
            print(data)
            user.login = data['group_id']
            user.botname = data['api_id']
            return open(file='index.html', encoding='utf8')

        else:
            print(data)
            print('login = ' + user.login)
            print('botname = ' + user.botname)
            return json.dumps({'login': user.login, 'botname': user.botname}, sort_keys=True)


@cherrypy.expose
class getWidget(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        widget ='<!— VK Widget —>\n<div id="vk_community_messages"></div>\n<script type="text/javascript">\n' \
                'VK.Widgets.CommunityMessages("vk_community_messages", '
        widget_r = ' , {expanded: "1",tooltipButtonText: "Есть вопрос?"});\n</script>'
        result = widget + user.login + widget_r
        return result

@cherrypy.expose
class upMoney(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **data):
        dbase.updateBalance(login=user.login, new=data['money'])
        return 'OK'

@cherrypy.expose
class BotStatus(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **data):
        dbase.upBot(data['login'], data['mode'])
        upBot(data['login'], data['mode'])
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

cherrypy.config.update({'server.socket_host': '31.31.201.218',
                        'server.socket_port': 8050,
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
cherrypy.tree.mount(UpdateClient(), '/upMoney', conf)
cherrypy.tree.mount(getWidget(), '/getWidget', conf)

cherrypy.engine.start()
cherrypy.engine.block()


