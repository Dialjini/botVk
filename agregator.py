#--- Agregator -----
import sqlite3
import dbase
import const
import fnck
import  datetime
import time
import sletat
from datetime import datetime, date, timedelta
import random
import threading
from threading import Thread
import connectForStrings




class Agregator():
    def print(self):
        message = 'Страна {0}\nКурорт {1}\nГород {2}\nНочи {3}\nКол-во {4}\nДети {5}\nДата: {6}\nЦена: {7}'.format(self.country, self.resort, self.city, self.nit, self.tur, self.kids, self.data, self.price)
        print(message)

    def detectStar(self):
        print('--Определение Звездности--')

    def detectMeal(self):
        print('--Определение питания--')

    def detectTuist(self):
        print('--Определение состава туристов--')
        keys = ['взрослых', 'человек', 'взрослый', 'взрослого', 'человека', 'взр', 'чел']
        cool = ['на двоих', 'на 2х', 'на 2 х', 'пара' 'две девушки', 'молодожены', 'вдвоем', 'двое', 'для двоих']
        for k in keys:
            self.text = self.text.replace(k, ' vz ')
        for k in cool:
            self.text = self.text.replace(k, ' tz ')
        ar = self.text.split(' ')
        print(self.text)
        try:
            index= ar.index('vz')
            while index>0:
                index -= 1
                try:
                    self.tur = int(ar[index])
                    ni = self.text.index('v')
                    while ni>0:
                        ni -=1
                        if self.text[ni]==str(self.tur):
                            self.text = self.text[0:ni] + self.text[ni+1:]
                            break
                    break
                except Exception:
                    continue
        except Exception:
            o=0

        try:
            a= ar.index('tz')
            self.tur = 2
        except Exception:
            o=0


    def detectPrice(self):
        print('--Определение бюджета--')
        keys= ['тыс', 'руб', ' 000']
        for k in keys:
            self.text = self.text.replace(k, ' pt ')
        ar = self.text.split(' ')
        for i in ar:
            try:
                if int(i)> 10000:
                    self.price = int(i)
                    self.text = self.text.replace(i, '')
                    break
            except Exception:
                continue
        if self.price == 0:
            try:
                index = ar.index('pt')
                while index>0:
                    index -=1
                    try:
                        if int(ar[index]) >0:
                            self.price = int(ar[index])
                            self.text = self.text.replace(ar[index], 'pwh')
                            break
                    except Exception:
                        continue
            except Exception:
                o=0
        if self.price>0 and self.price<1000:
            self.price *= 1000

    def delBe(self):

        keys = ['звезд', 'дети', 'детей', 'километров', 'лет', 'ребенок']
        for k in keys:
            self.text = self.text.replace(k, ' st ')

        ar = self.text.replace('или', '-').split(' ')
        tir=0
        bord = 0
        ino = 0
        try:
           index = self.text.index('s')
           ino = index
           while index>0:
               index -=1
               if self.text[index]=='-':
                   tir = 1
               try:
                   s = int(self.text[index])
                   if bord == 0:
                       bord = index
                   else:
                       if tir == 1:
                           bord = index
                           break
                       else:
                           break
               except Exception:
                   continue
        except Exception:
            d= 0

        if bord >0:
            self.text = self.text[0:bord] + self.text[ino:]



    def detectData(self):
        print('--Определение даты--')
        a = fnck.getData(self.text).replace('nill', '').replace('past', '')
        print(a)
        self.data = a

    def detectNit(self):
        print('--Определение количества ночей--')
        nu = ['ночей', 'ночь', 'дней', 'день']
        mi = ['до', 'или']
        for i in nu:
            self.text = self.text.replace(i, 'nite')
        for j in mi:
            self.text = self.text.replace(j, '-')
        tir = 0
        for i in self.text.replace('или', '-').replace('до', '-'):
            if i == '-':
                tir = 1
        ar = self.text.replace('или', '-').replace('до', '-').replace('-', ' - ').replace(',', ' ').replace('.', ' ').split( )
        # for i in ar:
        #     ar[ar.index(i)] = fnck.funDigit(i)
        nit = []
        tir = False
        nex = False
        try:
            index = ar.index('nite')
            nex = True
            while index >0:
                index -= 1
                if ar[index] == '-':
                    tir = True
                try:
                    nit.append(int(ar[index]))
                    if len(nit)> 2:
                        if tir:
                            break
                        else:
                            nit = [nit[0]]
                            break
                except Exception:
                    if len(nit)>0:
                        break

            for i in nit:
                if i>19:
                    nit.remove(i)

            if (nex and len(nit)==0):

                index = ar.index('nite')
                while index < len(ar):
                    index += 1
                    try:
                        nit =[int(ar[index])]
                        break
                    except Exception:
                        if len(nit) > 0:
                            break


            for h in nit:
                self.text = self.text.replace(str(h), '')
            if len(nit) == 2:

                if nit[0] > nit[1]:
                    e= nit[0]
                    nit[0] = nit[1]
                    nit[1] = e
                self.nit = str(nit[0]*100 + nit[1])
            else:
                self.nit = str(nit[0])
        except Exception:
            self.nit = 0


    def detectNort(self):
        print('--Определение направления--')

        check = fnck.creatNort(self.text, self.hotels)
        print(check)
        self.country = check['country']
        self.resort = check['resort']
        if int(self.resort) > 0:
            self.text = ''



    def detectCity(self):
        print('--Определение города вылета--')
        r = fnck.chekDepart(self.text)
        self.city = r


    def save(self):

        result = {'country': self.country, 'resort': self.resort, 'fromcity': self.city, 'nit': int(self.nit),'dataf': self.data, 'turistcount': self.tur, 'minPrice': self.price}
        for r in result:
            self.user[r] = result[r]
        try:
            dbase.userUpdate(value=self.user['country'], userid= self.user['userid'],
                                      collum='country', botname=self.user['botName'])
            dbase.userUpdate(value=self.user['fromc'], userid=self.user['userid'],
                                      collum='fromc', botname=self.user['botName'])
            dbase.userUpdate(value=self.user['resort'], userid= self.user['userid'],
                                      collum='resort', botname=self.user['botName'])
            dbase.userUpdate(value=self.user['nit'], userid=self.user['userid'],
                                      collum='nit', botname=self.user['botName'])
            dbase.userUpdate(value=self.user['turistcount'], userid=self.user['userid'],
                                      collum='count', botname=self.user['botName'])
            dbase.userUpdate(value=self.user['dataf'], userid=self.user['userid'],
                                      collum='date', botname=self.user['botName'])
            dbase.userUpdate(value=self.user['minPrice'], userid=self.user['userid'],
                                      collum='minPprice', botname=self.user['botName'])
        except Exception:
            pass

    def detect(self):
        self.detectNort()
        self.detectCity()
        self.detectPrice()
        self.detectNit()
        self.detectTuist()
        self.delBe()
        self.detectData()
        self.detectMeal()
        self.detectStar()
        self.print()
        self.save()


    def letsGo(self):
        self.detect()

    def __init__(self, text, user, hotels, botName):
        self.text = text
        self.base = text.split(' ')
        self.user = user
        self.hotels = hotels
        self.country = 0
        self.resort = 0
        self.city = 0
        self.data = ''
        self.nit = 0
        self.tur = 0
        self.kids = []
        self.price = 0
        self.botName = botName
