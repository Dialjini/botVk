from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
import vk_api
from PIL import Image
import tourBot
import dbase
import agregator
import connectForStrings as cStr
import requests
import random
from threading import Thread
import threading
import urllib.request
import os
from pathlib import Path

# 1+4+64+4096+131072+262144 = 397381

buffer = {}

def PhotoUpVk(vk, url='img.jpg'):
    return vk_api.upload.VkUpload(vk).photo_messages(url)

def savePhoto(photoUrl):
    i = requests.get(url=photoUrl, headers={'User-Agent': 'Mozilla/5.0'})
    img = urllib.request.urlopen(i.url).read()
    out = open("img.jpg", 'wb')
    out.write(img)
    out.close()
    out = open("img.jpg", 'wb')
    out.write(img)
    out.close()

    imgfile = Path("img.jpg")
    img = Image.open(imgfile)
    width = img.size[0]
    height = img.size[1]
    img3 = img.crop((0, 0, width, height - 53))
    img3.save("img.jpg")


def printUser(user):
    tss = ''
    for i in user:
        if i != 'tours':
            tss += i + ': ' + str(user[i]) + ' '
    print('user now ', tss)


class searchTours(Thread):
    def __init__(self, vk, user, botname, alter=False):
        Thread.__init__(self)
        self.vk = vk
        self.user = user
        self.botname = botname
        self.alter = alter

    def run(self):
        result = tourBot.SearchTour(self.user, self.botname)

        if self.alter:
            toursResr = result.alterRun()
        else:
            self.vk.messages.send(user_id=[self.user['username']], random_id=random.randint(0, 10000000),
                                 domain='public' + self.botname, message=cStr.waitImSearch)
            self.vk.messages.send(user_id=[self.user['username']], random_id=random.randint(0, 10000000),
                                  domain='public' + self.botname, message=cStr.textTourPerInfo)
            toursResr = result.run()
        dbase.updateStep(step=self.user['step'], username=self.user['username'], botname=self.botname)
        printUser(toursResr['userNew'])
        for i in toursResr['message']['attachment']:
            print('Flag - ', i)
            if i['url'] != 'none':

                try:
                    print('hotelId ' + str(i['url']))
                    savePhoto(i['url'])
                    up = PhotoUpVk(vk=self.vk)[0]
                    print('photo'+str(up['owner_id'])+'_'+str(up['id']))
                    self.vk.messages.send(message=i['text'], attachment='photo'+str(up['owner_id'])+'_'+str(up['id']), user_id=[self.user['username']], random_id=random.randint(0, 10000000))
                except Exception as er:
                    print(er, ' error upload and send photo')
                    print(i['text'] + i['url'])
                    self.vk.messages.send(message=i['text'] + i['url'], user_id=[self.user['username']], random_id=random.randint(0, 10000000))

            else:
                self.vk.messages.send(user_id=[self.user['username']], random_id=random.randint(0, 10000000),
                                      domain='public' + self.botname, message=i['text'])

        if toursResr['message']['text'] != '':
            self.vk.messages.send(user_id=[self.user['username']], random_id=random.randint(0, 10000000),
                                  domain='public' + self.botname, message=toursResr['message']['text'])
        if int(self.user['username']) not in buffer[self.botname]:
            buffer[self.botname][int(self.user['username'])] = {}
        if len(toursResr['userNew']['tours']) > 0:
            print('LAST STEP IN SEARCHTOURS')
            buffer[self.botname][int(self.user['username'])]['tours'] = toursResr['userNew']['tours']
            buffer[self.botname][int(self.user['username'])]['lastIndex'] = 3
        try:
            if 'date' in toursResr['userNew']['cashResult']:
                buffer[self.botname][self.user['username']]['cashResult'] = int(toursResr['userNew']['cashResult'])
            if 'userSorts' in toursResr['userNew']:
                buffer[self.botname][self.user['username']]['userSorts'] = toursResr['userNew']['userSorts']
        except Exception as er:
            print(er)


def updateMes(login, mes):
    dbase.lastMesUpdate(login=login, message=mes)

def polling(login, token):
    contact = dbase.getClientContacts(login)
    vk_session = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    buffer[login] = {}

    for event in longpoll.listen():
        if(dbase.timeToStop(login)):
            break
        if event.to_me:
            username = int(event.user_id)
            try:
                userinfo = dbase.getUserInfo(username, login)
                print('OK')
            except Exception as er:
                print(er)
                dbase.addNewUser(username=username, login=login)
                userinfo = {'resortsFordet': '0', 'tours': '0', 'lastIndex': '0', 'cashResult': 0, 'selectTour': '0',
                            'userSorts': '0', 'step': 'frstwaitrespons', 'botName': login, 'username': username,
                            'country': '0', 'resort': '0', 'fromcity': '0', 'date': '0', 'nit': 0, 'price': 0,
                            'adults': 0, 'children': 0, 'fromc': '0'}
            print(str(event.text) + ' ' + str(event.user_id))
            updateMes(login=username, mes=event.text)
            if username in buffer[login]:
                try:
                    if buffer[login][username]['type'] == 'resorts':
                        userinfo['resortsFordet'] = buffer[login][username]['arr']
                        print(userinfo['resortsFordet'])
                except Exception:
                    if 'tours' in buffer[login][username]:
                        userinfo['tours'] = buffer[login][username]['tours']
                        userinfo['lastIndex'] = buffer[login][username]['lastIndex']
                    if 'cashResult' in buffer[login][username]:
                        userinfo['cashResult'] = int(buffer[login][username]['cashResult'])
                    if 'selectTour' in buffer[login][username]:
                        userinfo['selectTour'] = buffer[login][username]['selectTour']
                    if 'userSorts' in buffer[login][username]:
                        userinfo['userSorts'] = buffer[login][username]['userSorts']

            result = tourBot.agregation(userinfo, login,
                   {'type': 'to_me', 'text': event.text}, contact)
            print(result['userNew']['step'], ' - result step')

            if result['userNew']['step'] == 'fire':
                sir_tour = searchTours(vk=vk, user=result['userNew'], botname=login)
                sir_tour.start()
            elif result['userNew']['step'] == 'fire2':
                sir_tour = searchTours(vk=vk, user=result['userNew'], botname=login, alter=True)
                sir_tour.start()
            else:
                if len(result['buffer']) > 0:
                    buffer[login][username] = result['buffer'][0]
                else:
                    if username in buffer[login]: del buffer[login][username]
                for i in result['message']['attachment']:
                    if i['url'] != 'none':
                        savePhoto(i['url'])
                        up = PhotoUpVk(vk=vk)[0]
                        print('up - ', up)
                        vk.messages.send(message=i['text'],
                                              attachment='photo' + str(up['owner_id']) + '_' + str(up['id']),
                                              user_id=[username], random_id=random.randint(0, 10000000))
                    else:
                        try:
                            vk.messages.send(user_id=[username], random_id=random.randint(0, 10000000),
                                            domain='public' + dbase.getBotname(login), message=i['text'])
                        except Exception as er:
                            print(er)
                if 'lastIndex' in result['userNew']:
                    try:
                        buffer[login][username]['lastIndex'] = result['userNew']['lastIndex']
                        buffer[login][username]['tours'] = result['userNew']['tours']
                    except Exception:
                        buffer[login][username] = {}
                        buffer[login][username]['lastIndex'] = result['userNew']['lastIndex']
                        buffer[login][username]['tours'] = result['userNew']['tours']
                try:
                    vk.messages.send(user_id=[username], random_id=random.randint(0, 10000000),domain='public' + login, message=str(result['message']['text']))
                except Exception:
                    print('er was result text = "' + result['message']['text'] + '"')
                dbase.fullUserUpdate(result['userNew'], username)

            if username not in buffer[login]:
                buffer[login][username] = {}

            if 'tours' in result['userNew']:
                buffer[login][username]['tours'] = result['userNew']['tours']
            if 'selectTour' in result['userNew']:
                buffer[login][username]['selectTour'] = result['userNew']['selectTour']
            if 'userSorts' in result['userNew']:
                try:
                    buffer[login][username]['userSorts'] = result['userNew']['userSorts']
                except Exception:
                    buffer[login][username] = {}
                    buffer[login][username]['userSorts'] = result['userNew']['userSorts']
            dbase.updateStep(step=result['userNew']['step'], username=username , botname=login)
            print('respons succesfull')
