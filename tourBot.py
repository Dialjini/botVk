
import connectForStrings
import cloudinary
from cloudinary import api, uploader, utils, config
import cloudinary.uploader
from urllib.request import Request, urlopen
import requests
import fnck
from agregator import Agregator
import datetime
from datetime import datetime, date, timedelta
from threading import Thread
import sletat
import MyDocs
import const


def cloudinary(name):
    config(
        cloud_name="ddnsfgt6o",
        api_key="777857854616732",
        api_secret="dthdx-XYltHZB_m2QUF7Gx4lLrA"
    )
    result = uploader.upload("Resort/{0}.jpg".format(name), crop="limit", tags="samples", width=700, height=700)
    print(result)
    return result['url']

class ComFunk():
    def __init__(self):
        print('iHere')

    def SortFrstBloc(self, toursC):
        print('frstSort')
        toursB = []
        h = []
        y = ''

        h.append(toursC[0]['HotelName'])
        toursB.append(toursC[0])
        for t in toursC:
            # print(str(t['HotelName']))
            try:
                y = h.index(str(t['HotelName']))
            except Exception:
                # print(t['OriginalHotelName'])
                h.append(t['HotelName'])
                if t['MealName'] != 'RO':
                    toursB.append(t)
        return toursB

    def grupedDictr(self, arr, param):
        result = {}
        for i in arr:
            try:
                result[i[param]].append(i)
            except Exception:
                result[i[param]] = [i]
        return result

class SearchTour():
    def __init__(self, us, botname):
        print('---init search tour---')
        self.user = us
        self.botName = botname
        self.usersTours = []
        self.result = {}



    def sevNit(self):
        result = []
        u = self.usersTours
        for i in u:
            if i['Nights'] == self.user['nit']:
                result.append(i)
        self.usersTours = result

    def extraSort(self, tours):
        print('=----------extraSort------------')
        result = []
        hotels = {}
        for i in tours:
            try:
                hotels[i['OriginalHotelName']].append(i)
            except Exception:
                hotels[i['OriginalHotelName']] = [i]

        for i in hotels:

            dataString = []
            nitString = []
            for j in hotels[i]:
                try:
                    g = dataString.index(fnck.butyDate(j['CheckInDate']))
                except Exception:
                    dataString.append(fnck.butyDate(j['CheckInDate']))
                try:
                    g = nitString.index(j['Nights'])
                except Exception:
                    nitString.append(j['Nights'])
            hotels[i][0]['dataString'] = dataString
            hotels[i][0]['nitString'] = nitString
            result.append(hotels[i][0])

        self.usersTours = result
        print('=----------extraSort END------------')


    def returnResult(self, message):
        self.user['tours'] = []

        return createResponse(result=self.result, user=self.user, step=self.user['step'], text= message)

    def fiesrPrint(self, upperText):

        print('my tours', len(self.usersTours))
        self.user['tours'] = self.usersTours
        self.result['message']['attachment'].append({'text': upperText, 'url': 'none'})
        for i in [0, 1, 2]:
            try:
                self.result['message']['attachment'].append(self.createAttach(self.usersTours[i], i))
            except Exception:
                # print(usersTours)
                continue
        self.user['lastIndexTour'] = 3

        message = 'Выберите номер тура, который больше нравится (цифрой). Или показать ещё?'
        self.result['message']['attachment'].append({'text': message, 'url': 'none'})

        return createResponse(result= self.result, user= self.user, step= self.user['step'], text= '')

    def grupedData(self, arr):

        result = ''
        grup = {}
        for i in arr:
            m = i.split(' ')
            print(m)
            try:
                grup[m[1]].append(m[0])
            except Exception:
                grup[m[1]] = [m[0]]

        for i in grup:
            a = ''
            o = str(grup[i]).replace('[', '').replace(']', '').replace("'", "")
            a = o + ' ' + i
            result += a
            result += ' '
        return result

    def createAttach(self, tour, index):
        user = self.user
        keyMeal = {'RO': 'без питания', 'BB': 'завтрак', 'HB': 'завтрак и ужин', 'AI': 'все включено',
                   'UIA': 'ультра все включено'}
        try:
            # if True:
            rating = ''
            try:
                if tour['HotelRating'] != 0.0:
                    rating = '\nРейтинг ' + str(tour['HotelRating'])

            except Exception:
                rating = ''

            meal = ''
            keyMeal = {'RO': 'без питания', 'BB': 'завтрак', 'HB': 'завтрак и ужин', 'AI': 'все включено',
                       'UIA': 'ультра все включено'}
            try:
                meal = keyMeal[tour['MealName']]
            except Exception:
                meal = tour['MealName']
            try:
                arr = tour['dataString']
                print()
                a = self.grupedData(arr)
                dS = '\nС вылетом ' + a
            except Exception as er:
                print('err create date ', er)
                dS = ''

            try:
                arr = tour['nitString']
                a = str(arr).replace('[', '').replace(']', '')
                nS = a
            except Exception:
                nS = tour['Nights']

            cururt = '\nКурорт: {0}'.format(tour['ResortName'])

            if self.botName == 'happyholidayclub':
                tour['Price'] = str(int(tour['Price'] * 0.99))

            if self.botName != 'ufagorturi' and self.botName != 'solyanka_travel':
                disf = '\n\n№{0}. {1} {2}\nВ номер: {3}\nПитание: {4}\nНа {5} ночей за {6}  ₽{7}'.format(index + 1,
                                                                                                         tour[
                                                                                                             'HotelName'] + ' ' +
                                                                                                         tour[
                                                                                                             'StarName'] + cururt,
                                                                                                         rating, tour[
                                                                                                             'OriginalRoomName'],
                                                                                                         meal, nS,
                                                                                                         fnck.butyPrice(
                                                                                                             int(tour[
                                                                                                                     'Price'])),
                                                                                                         dS).replace(
                    '₽' if self.botName == 'luxortourkz' else 'gg', '$')
            else:
                disf = '\n\n№{0}. {1} {2}\nВ номер: {3}\nПитание: {4}\nНа {5} ночей '.format(index + 1,
                                                                                             tour[
                                                                                                 'HotelName'] + ' ' +
                                                                                             tour[
                                                                                                 'StarName'] + cururt,
                                                                                             rating, tour[
                                                                                                 'OriginalRoomName'],
                                                                                             meal, nS)

            disf = disf.replace('₽', '$') if self.botName == 'luxortourk' else disf
            photoUrl = 'https://hotels.sletat.ru/i/im/{0}_{1}_670_447_0.jpg'.format(str(tour['HotelId']), 0)
            t = requests.get(photoUrl)
            print(type(t.status_code), t.status_code)
            if t.status_code != 200:
                photoUrl = 'https://pp.userapi.com/c846123/v846123027/10044/J54JTSSCbqA.jpg'
            print('NUKA ' ,{'text': disf, 'url': photoUrl})
            return  {'text': disf, 'url': photoUrl}
        except Exception as er:
            print(er)


    def getTourprice(self, tours):
        min = 0
        minTour = 0
        for tour in tours:

            if tour['CheckInDate'] != self.user['date'] and tour['Nights'] != self.user['nit']:
                print(tour['CheckInDate'], self.user['date'])
                print(tour['Nights'], self.user['nit'])
                print(tour['Price'])
                if min == 0:
                    print('zero')
                    return tour
                if int(tour['Price']) < int(min):
                    print('ebobob')
                    min = tour['Price']
                    minTour = tour
        print('minend')
        return minTour

    def frstSort(self, tours):
        result = []
        print('first sorting')
        allGood = []
        justGood = []
        nitGood = []
        dayGood = []
        minTour = self.getTourprice(tours)

        for tour in tours:

            if tour['CheckInDate'] == self.user['date'] and tour['Nights'] == self.user['nit'] and int(tour['Price']) < int(self.user['price']):
                allGood.append(tour)
            elif tour['CheckInDate'] == self.user['date'] and tour['Nights'] == int(self.user['nit']):
                # print(tour['Price'])
                justGood.append(tour)
            elif tour['Nights'] == self.user['nit'] and int(tour['Price']) < int(self.user['price']):
                nitGood.append(tour)
            elif tour['CheckInDate'] == self.user['date'] and int(tour['Price']) < int(self.user['price']):
                dayGood.append(tour)

        if self.user['price'] == 0 and len(justGood) > 0:
            print(len(justGood))
            print(justGood[0]['Price'])
            return [justGood, 'allGood']

        if len(allGood) > 0:
            print('allgood')

            return [allGood + justGood, 'allGood']
        else:
            if len(justGood) > 0:
                print('good')
                result.append(justGood)
                if len(nitGood) > 0:
                    result.append(nitGood[0])
                else:
                    result.append([])
                if len(dayGood) > 0:
                    result.append(dayGood[0])
                else:
                    result.append([])
                if minTour['Price'] < self.user['price']:
                    result.append(minTour)
                else:
                    result.append([])
                result.append('allNorm')
            else:
                try:
                    print(minTour['Price'])
                except Exception:
                    prii = 0
                print('so-so alha')


                try:
                    result.append(nitGood[0])
                except Exception:
                    result.append([])
                try:
                    result.append(dayGood[0])
                except Exception:
                    result.append([])

                try:
                    if int(minTour['Price']) < int(self.user['price']):
                        result.append(minTour)
                    else:
                        result.append(minTour)
                except Exception:
                    result.append([])
                result.append('allBad')
        # print(result)
        return result

    def createMidMessage(self, arr, price, nit, data):
        messageMid = ''
        # print('start create message', arr)
        for i in arr:

            try:
                a = ''
                if data:
                    a += 'с {0} '.format(fnck.butyDate(i['CheckInDate']))
                if nit:
                    try:
                        a += 'на {0} ночей '.format(str(i['arrNit']).replace('[', '').replace(']', ''))
                    except Exception:
                        a += 'на {0} ночей '.format(i['Nights'])
                if price:
                    a += 'от {0} ₽'.format(fnck.butyPrice(i['Price'])).replace('₽' if self.botName == 'luxortourkz' else 'gg', '$')
                a += '\n'
                messageMid += a
            except Exception as er:
                print(er)
                continue
        print('end create message', messageMid)
        return messageMid

    def fourBloc(self, tours):
        print('startFourBloc')
        peopleString = ''
        childString = ''
        if self.user['adults'] == 1:
            peopleString = 'одного взрослого'
        else:
            peopleString = '{0} взрослых'.format(self.user['adults'])
        if len(self.user['children']) != 0:
            if len(self.user['children']) == 1:
                childString = ' и один ребенок'
            else:
                childString = ' и {0} ребенка'.format(len(self.user['children']))
        resTurists = peopleString + childString

        infoReq = self.fourSort(tours)
        if infoReq[-1] == 'allNorm':
            print('---------norm----------')
            messageTop = 'Есть туры {0}-{1} для \n{2} по вашему запросу.'.format(
                fnck.nameCity(self.user['fromcity']), fnck.nameCountry(self.user['country']), resTurists)


            # self.vk.messages.send(message=messageTop, user_id=self.user['userid'])
            self.extraSort(tours)

            print('---------ex Sort--------------')
            if self.user['price'] != 0:
                self.sort('StarId', self.usersTours)

            self.user['step'] = 'waitZakaz'
            return  self.fiesrPrint(messageTop)


        elif infoReq[-1] == 'allBad':
            print('---------all fourBlock bad----------')
            messageTop = 'Туров в ваш бюджет нет (\n\nНо я нашла туры {0}-{1} для {2} по вашему запросу:'.format(
                fnck.nameCity(self.user['fromcity']), fnck.nameCountry(self.user['country']), resTurists)
            # self.vk.messages.send(message=messageTop, user_id=self.user['userid'])
            if len(infoReq[0]) == 1:


                self.creatGood(tours, messageTop)

            else:
                messageMid = self.createMidMessage(infoReq[0], True, True, True)

                message = '{0}\n\n{1}\nКакую дату вылета и длительность будем смотреть?'.format(
                    messageTop, messageMid)
                # self.vk.messages.send(message=message, user_id=self.user['userid'])
                ma = infoReq[0]
                dats = [self.user['date']]
                nits = [self.user['nit']]
                for i in ma:
                    try:
                        dats.append(i['CheckInDate'])
                        nits.append(i['Nights'])
                    except Exception:
                        print('->')
                        continue
                self.user['cashResult'] = {'date': dats, 'nit': nits}
                # usersSorts[str(self.user['userid'])] = 'non'
                print('logs - - - - - - ')
                print(self.user['cashResult'])

                self.user['step'] = 'wainIndef'
                return self.returnResult(message)

        else:
            print('---------bad----------')

            messageTop = 'Туров в ваш бюджет нет ('
            # self.vk.messages.send(message=messageTop, user_id=self.user['userid'])
            self.extraSort(tours)

            print('---------ex Sort--------------')

            message='Туров в ваш бюджет нет (\nПокажу туры в бюджет, начиная с лучших по звездности и рейтингу.'
            self.user['step'] = 'waitZakaz'
            return self.fiesrPrint(message)


    def nitsFromOneDate(self, arr):

        result = []

        for i in arr:
            yes = True
            for j in result:
                if i['Nights'] == j:
                    yes = False
            if yes:
                result.append(i['Nights'])
        return result

    def fourSort(self, tours):
        goodArr = {}
        bedArr = {}

        if self.user['price'] == 0:
            return ['allNorm']

        for tour in tours:

            if tour['Price'] < self.user['price']:
                try:
                    goodArr[str(tour['CheckInDate'])].append(tour)
                except Exception:
                    goodArr[str(tour['CheckInDate'])] = [tour]
            else:
                try:
                    bedArr[str(tour['CheckInDate'])].append(tour)
                except Exception:
                    bedArr[str(tour['CheckInDate'])] = [tour]

        goodPrice = []
        goodDay = []
        badAll = []

        for i in goodArr:
            goodArr[i][0]['arrNit'] = self.nitsFromOneDate(goodArr[i])
            goodPrice.append(goodArr[i][0])

        for i in bedArr:
            bedArr[i][0]['arrNit'] = self.nitsFromOneDate(bedArr[i])
            badAll.append(bedArr[i][0])

        result = []

        if len(goodPrice) != 0:
            return [goodPrice, 'allNorm']
        elif len(badAll) != 0:
            return [badAll, 'allBad']
        else:
            return ['nothing']

    def thBloc(self, tours):
        print('startThBloc')
        peopleString = ''
        childString = ''
        if self.user['adults'] == 1:
            peopleString = 'одного взрослого'
        else:
            peopleString = '{0} взрослых'.format(self.user['adults'])
        if len(self.user['children']) != 0:
            if len(self.user['children']) == 1:
                childString = ' и один ребенок'
            else:
                childString = ' и {0} ребенка'.format(len(self.user['children']))
        resTurists = peopleString + childString
        resReq = self.thSort(tours)
        # print(resReq)
        if len(resReq) == 1:
            messageTop = 'Есть туры {0}-{1} для {2} на {3} ночей: '.format(
                fnck.nameCity(self.user['fromcity']), fnck.nameCountry(self.user['country']), resTurists, self.user['nit'])
            # self.vk.messages.send(message=messageTop, user_id=self.user['userid'])
            self.extraSort(self.cutNit(tours))
            print('long after extra sort', len(self.usersTours))
            # self.sevNit()

            print('---------ex Sort--------------')

            self.sort('StarId', self.usersTours)
            print('long after extra General sort', len(self.usersTours))

            # self.fiesrPrint()
            self.user['step'] = 'waitZakaz'
            return self.fiesrPrint(messageTop)


        else:
            if len(resReq[0]) != 0:

                if len(resReq[1]) == 0 and self.user['price'] != 0:
                    messageZero = 'Хм.. у туроператоров нет таких туров.\n\nА я'

                else:
                    messageZero = 'Итак. Я'

                messageTop = '{0} нашла туры {1}-{2} для {3} на {4} ночей.'.format(messageZero,
                                                                                   fnck.nameCity(self.user['fromcity']),
                                                                                   fnck.nameCountry(
                                                                                       self.user['country']),
                                                                                   resTurists,
                                                                                   self.user['nit'])

                messageMidOne = self.createMidMessage(resReq[0], True, False, True)
                messageMid = self.createMidMessage(resReq[1], False, True, True)

                if len(resReq[1]) > 0:
                    messageMore = 'Есть туры и в ваш бюджет {0} ₽:'.format(self.user['price'])
                else:
                    messageMore = ''

                message = '{0}\n{1}\n\n{2}\n{3}\nКакую дату вылета смотреть?'.format(
                    messageTop, messageMidOne, messageMore, messageMid)
                # self.vk.messages.send(message=message, user_id=self.user['userid'])
                self.user['userSorts'] = 'non'
                ma = resReq[0] + resReq[1]
                dats = []
                nits = [self.user['nit']]
                for i in ma:
                    try:
                        print(i['CheckInDate'])
                        dats.append(i['CheckInDate'])
                        nits.append(i['Nights'])
                    except Exception:
                        continue

                self.user['cashResult']= {'date': dats, 'nit': nits}
                self.user['step'] = 'waitSData'
                return self.returnResult(message)
            else:
                try:
                    messageTop = 'Так. У туроператора нет туров {0}-{1} для {2} с вылетом {3}\nНо я нашла туры: '.format(
                        fnck.nameCity(self.user['fromcity']), fnck.nameCountry(self.user['country']), resTurists,
                        '{0}-{1}'.format(fnck.butyDate(self.user['date'].split('/')[0]), fnck.butyDate(self.user['date'].split('/')[1])))
                except Exception:
                    messageTop = 'Так. У туроператора нет туров {0}-{1} для {2} с вылетом {3}\nНо я нашла туры: '.format(
                        fnck.nameCity(self.user['fromcity']), fnck.nameCountry(self.user['country']), resTurists,
                        self.user['date'])

                if len(resReq[1]) == 1 :
                    self.extraSort(tours)
                    # self.vk.messages.send(message=messageTop, user_id=self.user['userid'])
                    return self.creatGood(tours, messageTop)

                else:

                    messageMid = self.createMidMessage(resReq[1], True, True, True)

                    message = '{0}\n\nНо я нашла похожие туры: \n{1}\nКакую дату вылета и длительность будем смотреть?'.format(
                        messageTop, messageMid)
                    # self.vk.messages.send(message=message, user_id=self.user['userid'])

                    ma = resReq[0] + resReq[1]
                    dats = [self.user['date']]
                    nits = [self.user['nit']]
                    for i in ma:
                        try:
                            dats.append(i['CheckInDate'])
                            nits.append(i['Nights'])
                        except Exception:
                            continue
                    self.user['cashResult'] = {'date': dats, 'nit': nits}

                    self.user['step'] = 'wainIndef'
                    return self.returnResult(message)

    def thSort(self, tours):

        goodArr = {}
        bedArr = {}

        print('th sort before dis')
        for tour in tours:
            print(tour['Price'], tour['Nights'], tour['CheckInDate'])
            if tour['Nights'] == self.user['nit']:
                try:
                    goodArr[str(tour['CheckInDate'])].append(tour)
                except Exception:
                    goodArr[str(tour['CheckInDate'])] = [tour]
            if tour['Nights'] != self.user['nit'] and tour['Price'] < self.user['price']:
                try:
                    bedArr[str(tour['CheckInDate'])].append(tour)
                except Exception:
                    bedArr[str(tour['CheckInDate'])] = [tour]

        goodPrice = []
        goodDay = []
        badAll = []
        print('th sort after dis')

        for i in goodArr:

            if goodArr[i][0]['Price'] < self.user['price']:
                goodPrice.append(goodArr[i][0])
            else:
                goodDay.append(goodArr[i][0])
        for i in bedArr:

            if bedArr[i][0]['Price'] < self.user['price']:
                bedArr[i][0]['arrNit'] = self.nitsFromOneDate(bedArr[i])
                badAll.append(bedArr[i][0])

        result = []
        print(len(goodPrice), 'goodP')
        print(len(goodDay), 'goodDay')
        print(len(badAll), 'baaad')

        if len(goodPrice) != 0:
            return [goodPrice]
        else:
            return [goodDay, badAll]

    def scndSort(self, tours):
        nMin = int(self.user['nit'] / 100)
        nMax = self.user['nit'] - nMin * 100
        goodArr = {}
        bedArr = {}
        i = nMin
        while i <= nMax:
            goodArr[str(i)] = []
            bedArr[str(i)] = []
            i += 1

        for tour in tours:
            if tour['CheckInDate'] == self.user['date']:
                goodArr[str(tour['Nights'])].append(tour)
            if (tour['CheckInDate'] != self.user['date'] and tour['Price'] < self.user['price']) or (
                    tour['CheckInDate'] != self.user['date'] and self.user['price'] == 0):
                bedArr[str(tour['Nights'])].append(tour)

        goodPrice = []
        goodDay = []
        badAll = []

        print(len(goodArr), len(bedArr))

        for i in goodArr:
            try:
                print(goodArr[i][0]['Price'])
                if goodArr[i][0]['Price'] < self.user['price']:
                    goodPrice.append(goodArr[i][0])
                else:
                    goodDay.append(goodArr[i][0])
            except:
                continue
        for i in bedArr:
            try:
                badAll.append(bedArr[i][0])
            except Exception:
                continue

        result = []
        # print(goodPrice)
        # print(goodDay)
        # print(badAll)
        if self.user['price'] == 0:
            return [goodDay, []]

        if len(goodPrice) != 0:
            return [goodPrice]
        else:
            return [goodDay, badAll]

    def scndBloc(self, tours):
        print('startScndBloc')
        peopleString = ''
        childString = ''
        if self.user['adults'] == 1:
            peopleString = 'одного взрослого'
        else:
            peopleString = '{0} взрослых'.format(self.user['adults'])
        if len(self.user['children']) != 0:
            if len(self.user['children']) == 1:
                childString = ' и один ребенок'
            else:
                childString = ' и {0} ребенка'.format(len(self.user['children']))
        resTurists = peopleString + childString
        resReq = self.scndSort(tours)
        # print(resReq)
        print(len(resReq))
        if len(resReq) == 1:
            print('variant 1')
            messageTop = 'Есть туры {0}-{1} для {2} с вылетом {3}: '.format(
                fnck.nameCity(self.user['fromcity']), fnck.nameCountry(self.user['country']), resTurists,
                fnck.butyDate(self.user['date']))
            print(len(resReq[0]), 'long result')
            if len(resReq[0]) == 1:
                # self.vk.messages.send(message=messageTop, user_id=self.user['userid'])
                return self.creatGood(self.filtrOnlyPrice(tours), messageTop)

            else:
                messageMid = self.createMidMessage(resReq[0], True, True, False)

                message = '{0}\n\n{2}\nНа какое количество ночей будем смотреть?'.format(
                    messageTop, self.user['price'], messageMid)
                # self.vk.messages.send(message=message, user_id=self.user['userid'])
                ma = resReq[0]
                dats = [self.user['date']]
                nits = [self.user['nit']]
                for i in ma:
                    try:
                        dats.append(i['CheckInDate'])
                        nits.append(i['Nights'])
                    except Exception:
                        continue

                self.user['cashResult']  = {'date': dats, 'nit': nits}
                self.user['step'] = 'waitSNit'
                print(message, 'message bf return')
                return self.returnResult(message)
        else:
            print('variant 2')
            if len(resReq[0]) != 0:
                print('wth now')
                if len(resReq[1]) == 0 and self.user['price'] != 0:
                    messageZero = 'Хм.. у туроператоров нет таких туров.\n\nА я'

                else:
                    messageZero = 'Итак. Я'

                messageTop = '{0} нашла туры {1}-{2} для {3} с вылетом {4}.'.format(messageZero,
                                                                                    fnck.nameCity(self.user['fromcity']),
                                                                                    fnck.nameCountry(
                                                                                        self.user['country']),
                                                                                    resTurists,
                                                                                    fnck.butyDate(self.user['date']))

                messageMidOne = self.createMidMessage(resReq[0], True, True, False)
                messageMid = self.createMidMessage(resReq[1], False, True, True)

                if len(resReq[1]) != 0:
                    messageMore = '\nЕсть туры и в ваш бюджет {0} ₽:\n{1}'.format(fnck.butyPrice(self.user['price']),
                                                                                  messageMid)
                    ques = 'дату вылета или'
                    self.user['step'] = 'wainIndefOr'
                else:
                    self.user['userSorts'] = 'non'
                    messageMore = ''
                    ques = ''
                    self.user['step'] = 'waitSNit'

                message = '{0}\n{1}\n{2}\nКакую {3} длительность будем смотреть?'.format(
                    messageTop, messageMidOne, messageMore, ques)
                # self.vk.messages.send(message=message, user_id=self.user['userid'])
                dats = [self.user['date']]
                nits = [self.user['nit']]
                ma = resReq[0] + resReq[1]

                for i in ma:
                    try:
                        dats.append(i['CheckInDate'])
                        nits.append(i['Nights'])
                    except Exception:
                        continue

                self.user['cashResult'] = {'date': dats, 'nit': nits}
                return self.returnResult(message)
            else:
                messageTop = 'Хм.. у туроператоров нет туров {0}-{1} для {2} с вылетом {3}: '.format(
                    fnck.nameCity(self.user['fromcity']), fnck.nameCountry(self.user['country']), resTurists,
                    fnck.butyDate(self.user['date']))
                print(messageTop)
                print(resReq)
                if len(resReq[1]) == 1:

                    self.creatGood(tours, messageTop)
                    # self.vk.messages.send(message= messageTop + '\nНо я нашла похожие туры:', user_id=self.user['userid'])
                else:
                    print('huli to')
                    messageMid = self.createMidMessage(resReq[1], True, True, True)
                    print(messageMid)
                    if len(resReq[1]) != 0:
                        message = '{0}\nНо я нашла похожие туры: \n{2}\nКакую дату вылета и длительность будем смотреть?'.format(
                            messageTop, self.user['price'], messageMid)
                        # self.vk.messages.send(message=message, user_id=self.user['userid'])
                        ma = resReq[1]
                        dats = [self.user['date']]
                        nits = [self.user['nit']]
                        for i in ma:
                            try:
                                dats.append(i['CheckInDate'])
                                nits.append(i['Nights'])
                            except Exception:
                                continue

                        self.user['cashResult'] = {'date': dats, 'nit': nits}
                        self.user['step'] = 'wainIndef'
                        return self.returnResult(message)
                    else:
                        # self.vk.messages.send(message= messageTop, user_id=self.user['userid'])
                        return self.returnResult(messageTop)

    def creatGood(self, tours, message = ''):
        if self.user['price'] != 0:
            self.sort(param='StarId', tours=tours)
        self.user['step'] = 'waitZakaz'

        self.usersTours = tours
        return self.fiesrPrint(message)




    def filtrOnlyPrice(self, tours):
        result = []
        for t in tours:
            if t['Price'] < self.user['price']:
                result.append(t)
        return result

    def firstBloc(self, tours):
        print('startFrstBloc')
        peopleString = ''
        childString = ''
        if self.user['adults'] == 1:
            peopleString = 'одного взрослого'
        else:
            peopleString = '{0} взрослых'.format(self.user['adults'])
        if len(self.user['children']) != 0:
            if len(self.user['children']) == 1:
                childString = ' и один ребенок'
            else:
                childString = ' и {0} ребенка'.format(len(self.user['children']))
        resTurists = peopleString + childString

        infoReq = self.frstSort(tours)
        if infoReq[-1] == 'allNorm':
            print('---------norm----------')
            secBloc = False
            if len(infoReq[1]) == 0 and len(infoReq[2]) == 0 and len(infoReq[3]) == 0:
                messageZero = 'Хм.. у туроператоров нет таких туров.\n\nА я нашла'

            else:
                messageZero = 'Есть'
                secBloc = True

            messageTop = '{0} туры {1}-{2} для {3} на {4} ночей с вылетом {5} от {6} ₽.'.format(messageZero,
                                                                                                 fnck.nameCity(
                                                                                                     self.user[
                                                                                                         'fromcity']),
                                                                                                 fnck.nameCountry(
                                                                                                     self.user[
                                                                                                         'country']),
                                                                                                 resTurists,
                                                                                                 self.user['nit'],
                                                                                                 fnck.butyDate(
                                                                                                     self.user[
                                                                                                         'date']),
                                                                                                 fnck.butyPrice(
                                                                                                     infoReq[0][0][
                                                                                                         'Price']))

            if secBloc:
                ma = [infoReq[1], infoReq[2], infoReq[3]]
                messageMid = self.createMidMessage([infoReq[1], infoReq[2], infoReq[3]], False, True, True)

                message = '{0}\n\nА я нашла туры в твой бюджет {1} ₽:\n{2}\nКакую дату вылета будем смотреть?'.format(
                    messageTop, self.user['price'], messageMid)
                # self.vk.messages.send(message=message, user_id=self.user['userid'])
                dats = [self.user['date']]
                nits = [self.user['nit']]

                for i in ma:
                    try:
                        dats.append(i['CheckInDate'])
                        nits.append(i['Nights'])
                    except Exception:
                        continue
                self.user['cashResult'] = {'date': dats, 'nit': nits}
                self.user['step'] = 'waitSData'
                return self.returnResult(message)

            else:
                # self.vk.messages.send(message=messageTop, user_id=self.user['userid'])

                self.usersTours = infoReq[0]


                if self.user['price'] != 0:

                    self.sort(param='StarId', tours=infoReq[0])
                self.extraSort(infoReq[0])
                self.user['step'] = 'waitZakaz'
                return self.fiesrPrint(messageTop)




        elif infoReq[-1] == 'allBad':
            print('---------bad frst block----------')
            print(self.user)
            messageTop = 'Так... у туроператоров нет туров {0}-{1} для {2} на {3} ночей с вылетом {4} до {5} ₽.'.format(fnck.nameCity(self.user['fromcity']), fnck.nameCountry(self.user['country']), resTurists,self.user['nit'], fnck.butyDate(self.user['date']), fnck.butyPrice(int(self.user['price'])))

            ma = [infoReq[0], infoReq[1], infoReq[2]]
            # print(infoReq[3])
            print('----------------------')
            if len(infoReq[2]) == 0:
                ree = 0
            else:
                ree = 1

            print(len(infoReq[0]) + len(infoReq[1]) + ree )
            messageMid = self.createMidMessage([infoReq[0], infoReq[1], infoReq[2]], True, True, True)
            if len(infoReq[0]) + len(infoReq[1]) + ree == 1:
                print('thi tRue')
                return self.creatGood(tours, messageTop + '\nНо я нашла похожие туры:')
                # self.vk.messages.send(message=messageTop + '\nНо я нашла похожие туры:', user_id=self.user['userid'])
            elif len(infoReq[0]) + len(infoReq[1]) + len(infoReq[2]) != 0:
                message = '{0}\nНо я нашла похожие туры: \n{2}\nКакую дату вылета будем смотреть?'.format(
                    messageTop, self.user['price'], messageMid)

                dats = []
                nits = []
                for i in ma:
                    try:
                        dats.append(i['CheckInDate'])
                        nits.append(i['Nights'])
                    except Exception:
                        continue
                self.user['cashResult'] = {'date': dats, 'nit': nits}
                self.user['step'] = 'waitSData'
                return self.returnResult(message)
            else:
                return self.returnResult(connectForStrings.mayBeAnotherdata)
        else:
            print('---------good----------')
            messageTop = 'Есть туры {0}-{1} для {2} на {3} ночей с вылетом {4} от {5} ₽.'.format(
                fnck.nameCity(self.user['fromcity']), fnck.nameCountry(self.user['country']), resTurists,
                self.user['nit'], fnck.butyDate(self.user['date']), fnck.butyPrice(infoReq[0][0]['Price']))

            print(len(infoReq[0]), '-----countGood-----')
            # self.usersTours = infoReq[0]
            self.extraSort(infoReq[0])
            if self.user['price'] != 0:
                self.sort(param='StarId', tours=infoReq[0])
            self.user['step'] = 'waitZakaz'
            self.user['cashResult'] = {}
            return self.fiesrPrint(messageTop)




    def cutNit(self, tours):
        result = []
        for i in tours:
            if i['Nights'] == self.user['nit']:
                result.append(i)

        return result

    def sortPrice(self, tours):

        while 1:
            trans = 0
            i=0
            while i<len(tours)-1:
                if tours[i]['Price'] > tours[i+1]['Price']:
                    c = tours[i]
                    tours[i] = tours[i+1]
                    tours[i+1] = c
                    trans += 1
                i+= 1
            if trans==0:
                break
        return tours

    def ratingSort(self, arr):

        while 1:
            trans = 0
            i = 0
            while i < len(arr) - 1:
                if arr[i]['HotelRating'] < arr[i + 1]['HotelRating']:
                    a = arr[i]
                    arr[i] = arr[i + 1]
                    arr[i + 1] = a
                    trans += 1
                i += 1
            if trans == 0:
                break
        return arr

    def strtSort(self, arr):
        print('start star sort')
        pr = {}
        result = []
        for i in arr:
            try:
                pr[str(i['StarId'])].append(i)
            except Exception:
                pr[str(i['StarId'])] = [i]
        print('create dictr')
        for i in pr:
            pr[i] = self.ratingSort(pr[i])
            result += pr[i]
        print('end star sort')
        return result

    def sort(self, param, tours):
        print('start sort')

        i = 0
        while 1:
            trans = 0
            i = 0
            while i < len(tours) - 1:

                if tours[i][param] < tours[i + 1][param]:
                    a = tours[i]
                    tours[i] = tours[i + 1]
                    tours[i + 1] = a
                    trans += 1
                i += 1

            if trans == 0:
                break
        toursG = []
        toursB = []

        print('--------logs sort----------')
        print('minPrice = ', self.user['price'])

        st = [404, 403, 402, 410]
        for k in st:
            for i in tours:

                if i['StarId'] == k:

                    if i['Price'] <= self.user['price']:
                        toursG.append(i)

                    else:
                        toursB.append(i)
        print('count good price tours = ', len(toursG))
        print('-----------------------------')
        # self.vk.messages.send(message='Покажу туры в бюджет, начиная с лучших по звездности и рейтингу.',
        #                       user_id=self.user['userid'])
        if len(toursG) > 1:

            buf = self.strtSort(toursG)
        else:
            buf = toursG

        self.usersTours = buf + toursB
        self.result['buffer'][0]['firstSort'] = ''
        print('----------end log sort-----------')

    def alterRun(self):
        try:
            user = self.user
            self.result = {
                'step': user['step'],
                'userNew': user,
                'message': {
                    'text': 'text',
                    'attachment': []
                },
                'buffer': []
            }
            print(user['resort'])
            user['hotel'] = 0
            print('start///////////////////////')
            # print(user['hotel'])
            print('/////////////////////////')
            try:
                if len(user['children']) == 0:
                    cld = []
                    print(cld)
                else:
                    print('kids', user['children'])
                    cld = user['children']
            except Exception:
                cld = []
            nit = user['nit']

            data = '{0}/{1}'.format(user['date'], user['date'])

            print(user['price'])
            usmin = user['price']
            usmin = int(0.6 * usmin)
            print(usmin, 'new -------------------')
            cv = ''
            if self.botName == 'hottour_minsk':
                cv = 'BYN'
            elif self.botName == 'luxortourkz':
                cv = 'USD'
            else:
                cv = 'RUB'

            try:
                toursC = sletat.getTours(user['fromcity'], user['country'], user['hotel'], nit, nit, user['adults'],
                                         data, len(cld), cld, user['resort'], usmin, cv)
            except Exception:
                toursC = sletat.getTours(user['fromcity'], user['country'], user['hotel'], nit, nit, user['adults'],
                                         data, len(cld), cld, user['resort'], 0, cv)
            sor = ComFunk()
            toursB = sor.SortFrstBloc(toursC)

            tours = []

            for t in toursB:
                if t['HotelRating'] > 5:
                    tours.append(t)
            print('----------before sort---------//')

            try:
                print(self.user['userSorts'])
                if self.user['userSorts'] != 'non':
                    try:
                        self.sort(param='StarId', tours=toursB)
                    except Exception:
                        self.usersTours = toursB
                else:
                    self.usersTours = toursB
                    self.user['userSorts'] = ''
            except Exception:
                self.usersTours = toursB
                self.user['userSorts'] = ''
            self.extraSort(self.usersTours)
            print(len(tours), 'всего есть')
            self.user['step'] = 'waitZakaz'
            self.user['lastIndex'] = 3

            return self.fiesrPrint('')



        except Exception as er:
            print('da kak tak to\n', er)

    def run(self):
        try:
            print('first request ---------')
            user = self.user
            user['price'] = int(user['price'])
            self.result = {
                'step': user['step'],
                'userNew': user,
                'message': {
                    'text': 'text',
                    'attachment': []
                },
                'buffer': []
            }
            self.result['buffer'].append({'firstSort': ''}) 

            print('id resort ', user['resort'])
            print('start///////////////////////')
            print('/////////////////////////')

            try:
                if len(user['children']) == 0:
                    cld = []
                    print(cld)
                else:
                    print('kids', user['children'])
                    cld = user['children']
            except Exception:
                cld = []

            if user['nit'] < 100:
                nitMin = user['nit'] + 2
                nitMax = user['nit'] - 2
            else:
                onee = int(user['nit'] / 100)
                two = user['nit'] - onee * 100
                if onee > two:
                    bu = onee
                    onee = two
                    two = bu
                nitMin = two
                nitMax = onee
            print(nitMin, nitMax)
            print('user mon price ', user['price'])
            # usmin = 0
            if int(user['price']) > 100000:
                usmin = int(0.95 * int(user['price']))
            else:
                usmin = 0
            print(usmin, 'new -------------------')

            if user['nit'] < 100:
                nitMin = int(user['nit'])
                nitMax = int(user['nit'])
            dateorSlet = user['date']
            if len(user['date'].split('/')) == 1:
                dateorSlet = '{0}/{1}'.format(user['date'], user['date'])

                
            cv = connectForStrings.curren[self.botName if self.botName in connectForStrings.curren else 'common'] 

            try:
                print('frst request')
                user['hotel'] = 0
                toursC = sletat.getTours(user['fromcity'], user['country'], user['hotel'], nitMin, nitMax,
                                         user['adults'],
                                         dateorSlet, len(cld), cld, user['resort'], usmin, cv)

                if user['nit'] < 100:
                    nitMin = user['nit'] + 2
                    nitMax = user['nit'] - 2
                dateorSlet = user['date']
                print('scnd requst')
                if user['price'] > 150000:
                    usmin = int(0.25 * user['price'])
                toursC += sletat.getTours(user['fromcity'], user['country'], user['hotel'], nitMin, nitMax,
                                          user['adults'],
                                          dateorSlet, len(cld), cld, user['resort'], usmin, cv)

            except Exception:
                print('-------try advancer-----')
                usmin = 0
                if user['nit'] < 100:
                    nitMin = user['nit'] + 2
                    nitMax = user['nit'] - 2
                dateorSlet = user['date']
                print(str(cld) + '  +++++++  ' + str(len(cld)))
                toursC = sletat.getTours(user['fromcity'], user['country'], user['hotel'], nitMin, nitMax,
                                         user['adults'],
                                         dateorSlet, len(cld), cld, user['resort'], usmin, cv)

            print(len(toursC), 'всего есть')

            toursC = self.sortPrice(toursC)


            if 0 != 0:
                print('goHot')
                user['tours'] = []
                user['tours'].append(toursC[0])
                for t in toursC:
                    cheche = 0
                    for tu in user['tours']:
                        if t['MealName'] == tu['MealName'] and t['HtPlaceName'] == tu['HtPlaceName']:
                            cheche = 1
                    if cheche == 0:
                        user['tours'].append(t)


                mes = ''
                i = 0
                for tour in user['tours']:
                    op = str(i) + '. ' + tour['HtPlaceName'] + ', ' + tour['MealName'] + ' - ' + fnck.devspace(
                        tour['Price']) + ' руб. \n'
                    mes += op
                    i += 1
                    if i > 10:
                        break
                self.userHotelTours[str(user['userid'])] = user['tours']
                self.vk.messages.send(message='Итак, я нашла лучшие варианты для тебя\n' + mes + 'сделай выбор числом',
                                      user_id=user['userid'])
                user['step'] = 'waitTourHotel'


            else:
                print('go')

                minBorder = 0.5
                midBorder = 0.2

                reHotels = {}
                toursS = []
                for i in toursC:
                    try:
                        a = reHotels[i['HotelName']]
                    except Exception:
                        reHotels[i['HotelName']] = i
                        toursS.append(i)

                tours = []

                for t in toursS:
                    if t['HotelRating'] > 5:
                        tours.append(t)

                peopleString = ''
                childString = ''

                if self.user['adults'] == 1:
                    peopleString = 'одного взрослого'
                else:
                    peopleString = '{0} взрослых'.format(self.user['adults'])
                try:
                    if user['children'][0] != '':
                        if len(user['children']) == 1:
                            childString = ' и один ребенок'
                        else:
                            childString = ' и {0} ребенка'.format(len(self.user['children']))
                except Exception:
                    childString = ''
                resTurists = peopleString + childString

                if len(user['date'].split('/')) == 1:
                    if user['nit'] < 100:
                        print('-/-/-/-/-/--/-/-/-/-/-')
                        return self.firstBloc(tours)
                    else:
                        return self.scndBloc(tours)
                else:
                    if user['nit'] < 100:
                        print('-/-/-/-/-/--/-/-/-/-/-')
                        return self.thBloc(tours)
                    else:
                        return self.fourBloc(tours)



        except Exception as er:
            print('\n\n\n', er, '\n\n\n')
            # self.vk.messages.send(
            #     message='Проверила всех туроператоров. Подходящие туры есть, но возможно, на другие даты вылета или продолжительность.',
            #     user_id=user['userid'])


            user['step'] = 'waitManeger'
            return self.returnResult('Туров на эти даты вылета или продолжительность я не нашла.\n\nНапишите "Менеджер" или "Новый" для продолжения')
            



def searchOnNit(n, user, result):
    allR = False
    for i in user['cashResult']['nit']:
        if i == n:
            allR = True
            break
    if allR:
        print('show must go on')
        user['nit'] = n
        user['step'] = 'fire2'
        return createResponse(result= result, user= user, step= user['step'], text= '')

    else:
        return createResponse(result=result, user=user, step=user['step'], text='Такой ночи я не предлагала')





def searchOnDate(l, user, result):
    allR = False
    print('cashResult', user['cashResult'])
    for i in user['cashResult']['date']:
        if i == l:
            allR = True
            break

    try:
        if not allR:
            for i in user['cashResult']['date']:
                print(l.split('.'), i.split('.'))
                if i.split('.')[0] == l.split('.')[0] and i.split('.')[1] == l.split('.')[1]:
                    allR = True
                    l = i
                    break
    except Exception:
        print()

    if not allR:
        for i in user['cashResult']['date']:
            print(i.split('.')[0], l)
            if int(i.split('.')[0]) == int(l.split(' ')[0]):
                l= i
                allR = True
                break



    if allR:
        user['step'] = 'fire2'
        user['dataf'] = l
        cs = user['cashResult']
        print(cs)
        user['nit'] = cs['nit'][cs['date'].index(l)]
        return createResponse(result, user, user['step'], '')
    else:

        return createResponse(result, user, user['step'], 'Такой даты я не предлагала')


def setStep(user):
    if user['fromcity'] == '0' or user['fromcity'] == 0:
        user['fromcity'] = '0'
        return 'waitCity'
    elif user['nit'] == 0:
        return 'waitNit'
    elif user['adults'] == 0 or user['adults'] == '0':
        user['adults'] = 0
        return 'waitAdult'
    # if str(user['children']) ==[]:
        # return 'waitKidsM'
    elif user['date'] == '0':
        return 'waitDate'
    elif user['price'] == 0:
        return 'waitMin'
    elif user['country'] == '0':
        return 'frstwaitrespons'
    else:
        return 'fire'


def nextStep(user, result):
    needSet = setStep(user)
    if needSet != 'fire':
        rexamp = ['18', '', '']
        examp = (datetime.now() + timedelta(days=30)).timetuple()
        for i in [1, 2]:
            if examp[i] < 10:
                rexamp[i] = '0' + str(examp[i])
            else:
                rexamp[i] = str(examp[i])
        keys = {
            'waitCity': 'Ок, {0}. Какой город вылета?'.format(
                fnck.nameCountry(user['country'])) if (str(user['resort']) == '0' or len(str(user['resort']).split('/'))>1) else 'Ок, {0}. Какой город вылета?'.format(
                fnck.nameTown(user['resort'])),
            'waitNit': 'Записала. А на какое количество ночей будет тур?'.format(
                fnck.nameCity(user['fromcity'])),
            'waitAdult': 'Сколько взрослых полетит?',
            'waitDate': 'Когда хотите вылетать? (например: {0}.{1})'.format(rexamp[2],
                                                                            rexamp[1]),
            'waitMin': 'Укажите бюджет, чтобы увидеть лучшие туры по звездности и рейтингу.\nИли напишите нет.'.replace(
                'рублях' if user['botName'] == 'luxortourkz' else 'gg', 'долларах'),
            'frstwaitrespons': 'Где хотите отдохнуть?'
        }

        user['step'] = needSet

        return createResponse(result=result, user=user, step=user['step'], text= keys[needSet])

    else:
        print('negoo')
        return createResponse(result=result, user=user, step= 'fire', text= '')
        # fnck.saveCountReq(namePub)
        # vk.messages.send(user_id=user['userid'],
        #                  message='Запрашиваю туры у {0} туроператоров и {1} авиакомпаний'.format(
        #                      random.randint(47, 64), random.randint(12, 15)))
        # time.sleep(5)
        # vk.messages.send(user_id=user['userid'],
        #                  message='Ищу самые выгодные, это займет 30 секунд...\nВ цену тура входит: перелет, проживание, страховка, трансфер и питание.')
        # user['step'] = 'nihua'
        # SQLmanager.saveRepsonData(value=user['step'], userid=user['userid'], botname=botName,
        #                           collum='step')
        # ser = SearchTour(vk_session, user, vk, botName, userHotelTours, [])
        # ser.start()

def detect_without_steps(text):
    pass


def start_text(user):
    pass


def createResponse(result, user, step, text):
    user['step'] = step
    result['userNew'] = user
    result['message']['text'] = text
    return result


def detectCountry(country, vari, user, result):
    resorts = fnck.resortsInfo(country)

    if len(resorts) < 2:
        if vari == 1:
            m = 'Так'
            user['step'] = 'waitCity'
        else:
            m = 'Ок'
            user['step'] = 'zero'

        text = connectForStrings.textCityFrom.format(m,
            fnck.nameCountry(user['country']))

    else:
        mesg = ''
        j = 1
        for i in resorts:
            mesg += '{0}. {1}\n'.format(j, i['resort'])
            j += 1
        if vari == 1:
            m = 'В этой стране'
            user['step'] = 'waitResortLon'
            result['buffer'] = [{'type': 'resorts', 'arr': resorts}]
        else:
            m = 'Ок, {0}. В этой стране '.format(fnck.nameCountry(user['country']))
            if len(resorts) == 0:
                user['step'] = 'waitCity'
            else:
                user['step'] = 'waitResortLon'
                result['buffer'] = [{'type': 'resorts', 'arr': resorts}]
        if len(resorts)>4:
            k = 'ов'
        else:
            k = 'а'

        text = connectForStrings.textArrResorts.format(m,
                len(resorts), k, mesg)

    result['step'] = user['step']
    result['message']['text'] = text
    result['userNew'] = user


    return createResponse(result= result, user= user, text= text, step= user['step'])


def obnul(user):
    user['country'] = '0'
    user['resort'] = '0'
    user['fromcity'] = '0'
    user['date'] = '0'
    user['nit'] = '0'
    user['price'] = '0'
    user['adults'] = '0'
    user['children'] = '0'
    user['nit'] = '0'


def showResortQuesto(user, result):
    resorts = fnck.resortsInfo(fnck.nameCountry(user['country']))
    if len(resorts) < 2:
        return nextStep(user, result)
    else:
        mesg = ''
        j = 1
        for i in resorts:
            mesg += '{0}. {1}\n'.format(j, i['resort'])
            j += 1

        m = 'В этой стране'
        user['step'] = 'waitResortLon'

        if len(resorts) > 4:
            k = 'ов'
        else:
            k = 'а'


        message='{0} Топ-{1} курорт{2}\n{3}\nЗнаете в какой ищем туры или посоветовать?'.format(m,
                                                                                                    len(
                                                                                                        resorts),
                                                                                                    k,
                                                                                                    mesg)

        result['buffer']= [{'type': 'resorts', 'arr': resorts}]
        return createResponse(result= result, user= user, step= user['step'], text= message)


def nextTourPrint(user, index, result):
    print('my tours', len(user['tours']))
    result['message']['attachment'].append({'text': '', 'url': 'none'})
    sr = SearchTour(user, user['botName'])
    for i in [user['lastIndex'], user['lastIndex'] + 1, user['lastIndex'] + 2]:
        try:
            result['message']['attachment'].append(sr.createAttach(user['tours'][i], i))
            user['lastIndex'] = i + 1
        except Exception as er:
            print('NextTourPrint Error: ', er)
            # print(usersTours)
            continue


    message = 'Выберите номер тура, который больше нравится (цифрой). Или показать ещё?'

    try:
        if (index + 2) >= len(user['tours']):
            message = 'Туров больше нет. Выберите номер тура, который больше нравится (цифрой)'
    except Exception as er:
        print(er, ' -error in nex print')
        message = 'Туров больше нет. Выберите номер тура, который больше нравится (цифрой)'


    result['message']['attachment'].append({'text': message, 'url': 'none'})
    return createResponse(result, user, user['step'], '')


def agregation(user, client, event, clientCon):

    result = {
        'step': user['step'],
        'userNew': user,
        'message': {
            'text': 'text',
            'attachment': []
        },
        'buffer': []
    }

    print(event)

    if event['type'] == 'to_me':

        for s in connectForStrings.words['Заново']:
            for g in event['text'].split(' '):
                if s.lower() == g.lower() and user['step'] != 'start':
                    obnul(user)
                    return createResponse(result= result, user= user, step= 'frstwaitrespons', text= connectForStrings.hellotext[user['botName'] if user['botName'] in connectForStrings.hellotext else 'simple'])


        for s in connectForStrings.words['manager']:
            for g in event['text'].split(' '):
                if s.lower() == g.lower():
                    return createResponse(result= result, user= user, step= 'waitPhone', text= connectForStrings.callManagerWithoutTour)
        print('user step = ', user['step'])
        if user['step'] != 'frstwaitrespons' and user['step'] != 'start' and user['step'] != 'waitLoh' and user[
            'step'] != 'waitCity' and user['step'] != 'nihua' and user['step'] != 'waitZakaz' and user[
            'step'] != 'waitDate' and user['step'] != 'waitSDate' and user['step'] != 'zeroReso' and user[
            'step'] != 'waitSData':
            for c in event['text'].replace('Добрый', 'привет').replace('добрый', 'привет').split(' '):
                # print(fnck.checkCountryTwo(c))
                sea = False
                for i in connectForStrings.words['sea']:
                    if c.lower() == i:
                        createResponse(result= result, user= user, step= 'searchSea', text= connectForStrings.textSea)
                        sea = True
                        break
                if sea:
                    break

                if fnck.checkCountryTwo(c) != 0 and c.lower() != 'бали':
                    user['country'] = fnck.codCountry(fnck.checkCountryTwo(c))
                    return detectCountry(fnck.checkCountryTwo(c), 2, user, result)
                    # return createResponse(result= result, user= user, step= user['step'], text= result['message']['text'])

                if user['step'] != 'waitResortLon':
                    d = fnck.checkResortHz(c)
                    print('chek resort1', user['step'])
                    print(d)
                    if len(d) != 0 and user['step'] != 'waitCity':
                        print('user data on time prestep scaning in resort ', user)
                        user['resort'] = d[0]
                        user['country'] = d[1]
                        return createResponse(result= result, user= user, text= 'Так, {0} {1}. Какой город вылета?'.format(
                            fnck.nameCountry(user['country']), fnck.nameTown(user['resort'])), step= 'waitCity')
                        break

        if user['step'] == 'start':
            try:
                agreg = Agregator(event['text'], user, [], user['botName'])
                agreg.letsGo()
            except Exception as er:
                print(er)


            return createResponse(result=result, user=user, step='frstwaitrespons', text=connectForStrings.hellotext[
                                                                                              user['botName'] if user[
                                                                                                                     'botName'] in connectForStrings.hellotext else 'simple'])


        elif user['step'] == 'frstwaitrespons':

            resultSea = ''
            sea = ['Море', 'море', 'Морской', 'морское', 'морской', 'Морское']
            for i in event['text'].split(' '):
                for j in sea:
                    if j == i:
                        resultSea = 'sea'

            if resultSea == 'sea':
                user['step'] = 'searchSea'
                return createResponse(result= result, step= user['step'], user= user, text= connectForStrings.textSea)


            else:
                agreg = Agregator(event['text'], user, [], user['botName'])
                agreg.letsGo()
                if user['country'] == 0 or user['country'] == '0':
                    user['country'] = 0
                    return createResponse(result= result, user= user, step= user['step'], text= connectForStrings.textResortOrCountry)

                else:
                    if user['resort'] == 0 or user['resort'] == '0':
                        user['resort'] = 0
                        return showResortQuesto(user, result)
                    else:
                        return nextStep(user, result)

        elif user['step'] == 'searchSea':

            try:

                for i in event['text'].split(' '):
                    if fnck.funDigit(i) != i:
                        event['text'] = fnck.funDigit(i)
                        break
                chus = int(event['text']) - 1

                list = ['Турция', 'Таиланд', 'Вьетнам', 'Кипр', 'Греция']
                user['country'] = fnck.codCountry(list[chus])
                return detectCountry(list[chus], 1, user, result)

            except Exception as er:
                print(er)
                return createResponse(result=result, user=user, step=user['step'],
                                      text=connectForStrings.noThink4Sea)


        elif user['step'] == 'searchResort':
            try:

                for i in event['text'].split():
                    if fnck.funDigit(i) != i:
                        event['text'] = fnck.funDigit(i)
                        break

                chus = int(event['text']) - 1
                print(user['cashResort'], 'resort list')
                for i in user['cashResort']:
                    print(i)
                    if i['id'] == user['userid']:
                        user['resort'] = fnck.codTown(i['data'][chus - 1][0])
                        user['country'] = i['data'][chus][1]
                        return createResponse(result= result, user= user, step= 'waitCity', text= connectForStrings.yesResortNeedCity.format(
                                    fnck.nameCountry(user['country']), i['data'][chus][0]))

            except Exception:
                return createResponse(result=result, user=user, step= user['step'],
                                      text=connectForStrings.iduKudaletim)


        elif user['step'] == 'waitResortLon':
            text = fnck.removeRepit(event['text'])
            arr = text.replace(',', ' ').replace('.', ' ').split(' ')
            try:
                rss = user['resortsFordet']
                print(rss, ' resort list')
            except Exception:
                rss = []
            resultR = []
            stopWord = []
            for i in arr:
                try:
                    r = rss[int(i) - 1]['resort']
                    print('ch resort', r)
                    if r == 'Адриатическая ривьера':
                        r = 'Римини'
                        resultR.append(fnck.codTown(r))
                    elif r == 'Венецианская ривьера':
                        s = ['Линьяно', 'Бибионе', 'Каорле', 'Лидо ди Езоло', 'Триест']
                        for i in s:
                            resultR.append(fnck.codTown(i))
                    else:
                        a = fnck.likeResort(r, user['country'])
                        resultR.append(fnck.codTown(a))
                    print(resultR, a, 'resort result')
                except Exception as er:
                    print(er)
                    for j in rss:
                        goN = True
                        for yy in stopWord:
                            if yy.lower() == i.lower():
                                goN = False
                        print(j['resort'].lower(), i.lower(), goN)
                        if fnck.fhot(j['resort'].lower(), i.lower()) == 1 and goN:

                            if j['resort'] == 'Адриатическая ривьера':
                                r = 'Римини'
                                resultR.append(fnck.codTown(r))
                            elif j['resort'] == 'Венецианская ривьера':
                                s = ['Линьяно', 'Бибионе', 'Каорле', 'Лидо ди Езоло', 'Триест']
                                for i in s:
                                    resultR.append(fnck.codTown(i))
                            else:
                                a = fnck.likeResort(j['resort'], user['country'])
                                resultR.append(fnck.codTown(a))
                            for h in j['resort'].split(' '):
                                stopWord.append(h)

            if len(resultR) != 0:
                user['resort'] = str(resultR).replace("'", '').replace("'", '').replace('[', '').replace(']',
                                                                                                        '').replace(',',
                                                                                                                    '/').replace(
                    ' ', '')
                print('result add in user resort ', user['resort'])
                mr = ''
                for i in resultR:
                    mr += fnck.nameTown(i) + ', '
                mr = mr.replace('Римини', 'Адриатическая ривьера').replace(
                    'Линьяно, Бибионе, Каорле, Лидо ди Езоло, Триест', 'Венецианская ривьера')


                user['resortsFordet'] = []
                print('resilt in result', result)
                print('user in resi ', user)
                return nextStep(user, result)

            else:
                gAw = False
                for i in connectForStrings.words['nothing']:
                    for j in text.split(' '):
                        if i.lower() == j.lower():
                            gAw = True
                if gAw:

                    return nextStep(user, result)

                else:

                    for i in connectForStrings.words['help']:
                        for j in text.replace('не знаю', 'незнаю').replace('Не знаю', 'незнаю').split(' '):
                            if fnck.fhot(i.lower(), j.lower()):
                                gAw = True
                    if gAw:
                        for i in user['resortsFordet']:
                            print(i)
                            try:
                                result['message']['attachment'].append({'text': '{0}\n{1}'.format(i['resort'], i['discript']), 'url': cloudinary(i['img'])})
                            except Exception as er:
                                print(er)
                                continue
                        return createResponse(result= result, user= user, step= user['step'], text= connectForStrings.vKaloyKurirt)

                    else:
                        d = fnck.checkResortHz(c)
                        print('chek resort2', user['step'])
                        print(d)
                        if len(d) != 0 and user['step'] != 'waitCity':
                            print('user data on time prestep scaning in resort ', user)
                            user['resort'] = d[0]
                            user['country'] = d[1]
                            user['hotel'] = 0
                            print(i)
                            return createResponse(result=result, user=user, step='waitCity',
                                                  text=connectForStrings.yesResortNeedCity.format(
                                                      fnck.nameCountry(user['country']), fnck.nameTown(user['resort'])))


                        else:
                            result['buffer'] = [{'type': 'resorts', 'arr': user['resortsFordet']}]
                            return createResponse(result=result, user=user, step= user['step'],
                                                  text=connectForStrings.iVkakoy)


        elif user['step'] == 'waitCity':
            user['fromcity'] = 0
            print('user data before save city ', user)
            text = event['text'].split(' ')
            for j in text:

                if j.lower() == 'омск':
                    user['fromcity'] = 1278
                    print('--------- nj', user['fromcity'], fnck.nameCity(user['fromcity']))
                    break

                if j.lower() == 'нск':
                    user['fromcity'] = fnck.codCity('Новосибирск')
                    print('--------- nj', user['fromcity'])
                    break

                if j.lower() == 'новгород':

                    if text[text.index(j) - 1].lower() == 'нижний' or text[text.index(j) - 1].lower() == 'н.' or \
                            text[text.index(j) - 1].lower() == 'н':
                        user['fromcity'] = fnck.codCity('Нижний Новгород')
                        print('--------- nj', user['fromcity'])
                        break
                    if text[text.index(j) - 1].lower() == 'великий':
                        user['fromcity'] = fnck.codCity('Великий Новгород')
                        print('--------- nj', user['fromcity'])
                        break
            print(text)
            for i in text:
                print(i)

                if fnck.checkCity(i) == 1 and len(i) > 2 and user['fromcity'] == 0:
                    user['fromcity'] = fnck.codCity(i.capitalize())
                    break
            if user['fromcity'] != 0 or user['fromcity'] != '0':

                return nextStep(user, result)

                print('user data after save city ', user)
            else:
                return createResponse(result= result, user= user, step= user['step'], text= connectForStrings.cityNoExist)

        elif user['step'] == 'waitNit':
            user['nit'] = 0

            a = event['text']
            b = ''
            i = 0
            while i < len(a):
                if a[i] >= 'а' and a[i] <= 'я':
                    print('')
                else:
                    b += a[i]
                i += 1

            nitCas = b.replace(' ', '-').split('-')
            nit = []
            for i in nitCas:
                i = fnck.funDigit(i)
                try:
                    nit.append(int(i))
                except Exception:
                    continue
            print('list nit', nit)
            try:
                print(len(nit))
                nite = 0
                if len(nit) == 1:
                    print(fnck.strToInt(nit[0]))
                    user['nit'] = fnck.strToInt(nit[0])
                elif len(nit) == 2:
                    user['nit'] = nit[0] * 100 + nit[1]
                else:
                    for n in nit:
                        try:
                            nite += fnck.strToInt(n)
                        except Exception:
                            OoO = 123
                    user['nit'] = fnck.strToInt(nite / nit.__len__())
                big = 0

                for i in nit:
                    if i > 20 or i < 2:
                        big = i

                if big == 0:

                    return nextStep(user, result)

                else:
                    return createResponse( result= result, user= user, step= user['step'], text= connectForStrings.textNitNotFormat)

            except Exception as er:
                print(er)
                return createResponse(result=result, user=user, step=user['step'],
                                      text=connectForStrings.nitNotitNotCount)

        elif user['step'] == 'waitTurist':
            text = event['text'].replace('-', ' ').split(' ')
            yes = False

            for i in text:
                i = fnck.funDigit(i)
                if i == '1' or i.capitalize() == 'Взрослый' or event['text'].capitalize().replace(' ', '') == 'я':
                    rexamp = ['18', '', '']
                    examp = (datetime.now() + timedelta(days=30)).timetuple()
                    for i in [1, 2]:
                        if examp[i] < 10:
                            rexamp[i] = '0' + str(examp[i])
                        else:
                            rexamp[i] = str(examp[i])

                    user['step'] = 'waitDate'
                    user['adults'] = 1
                    user['children'] = []
                    yes = True
                    return createResponse(result= result, user= user, step= user['step'], text= connectForStrings.textNeedDate.format(rexamp[2],
                                                                                                  rexamp[1]))
                    break
                if i == '2' or i.capitalize() == 'Два' or i.capitalize() == 'Двое':
                    rexamp = ['18', '', '']
                    examp = (datetime.now() + timedelta(days=30)).timetuple()
                    for i in [1, 2]:
                        if examp[i] < 10:
                            rexamp[i] = '0' + str(examp[i])
                        else:
                            rexamp[i] = str(examp[i])

                    user['step'] = 'waitDate'
                    user['adults'] = 2
                    user['children'] = []
                    return createResponse(result=result, user=user, step=user['step'],
                                          text=connectForStrings.textNeedDate.format(rexamp[2],
                                                                                     rexamp[1]))
                    yes = True
                    break
                if i == '3':

                    user['step'] = 'waitOneKid'
                    user['adults'] = 2
                    return createResponse(result=result, user=user, step=user['step'],
                                          text=connectForStrings.textNeedKit)



                    yes = True
                    break
                if i == '4':

                    user['step'] = 'waitAdult'
                    return createResponse(result=result, user=user, step=user['step'],
                                          text=connectForStrings.textHowMuchAdult)
                    yes = True
                    break
            if yes == False:
                return createResponse(result=result, user=user, step=user['step'],
                                      text=connectForStrings.iDontUnderstand)

        elif user['step'] == 'waitAdult':
            try:
                event['text'] = event['text'].replace('на двоих', '2').replace('Hа двоих', '2')
                event['text'] = fnck.funDigit(event['text'])
                user['adults'] = str(int(event['text']))
                user['step'] = 'waitKidsM'
                return createResponse(result=result, user=user, step=user['step'],
                                      text=connectForStrings.textHowMuchCild)


            except Exception as er:
                print(er)
                return createResponse(result=result, user=user, step=user['step'],
                                      text=connectForStrings.textNoAdult)


        elif user['step'] == 'waitKidsM':
            try:
                old = event['text'].replace(',', ' ').replace('.', ' ').replace('младенец', '1').split(' ')
                kil = []
                norm = True
                for i in old:
                    i = fnck.funDigit(i)
                    if i.lower() == 'месяц' or i.lower() == 'мксяцев':
                        kil = [1]
                        break
                    try:
                        if int(i) == 0:
                            continue
                        print('kiikiki', i)
                        if int(i) < 17 and int(i) >= 0:
                            print(int(i))
                            kil.append(int(i))
                        else:
                            print('wtf')
                            norm = False

                            return createResponse(result=result, user=user, step=user['step'],
                                                  text=connectForStrings.itsNotKid.format(i))

                    except Exception as er:
                        print(er)
                        continue

                user['children'] = kil

            except Exception:
                user['children'] = []

            if norm:
                rexamp = ['18', '', '']
                examp = (datetime.now() + timedelta(days=30)).timetuple()
                for i in [1, 2]:
                    if examp[i] < 10:
                        rexamp[i] = '0' + str(examp[i])
                    else:
                        rexamp[i] = str(examp[i])

                return nextStep(user, result)


        elif user['step'] == 'waitOneKid':

            try:

                for i in event['text'].split(' '):
                    i = fnck.checkInt(i)
                    try:
                        ev = int(fnck.funDigit(i))
                        break
                    except Exception:
                        continue

                if int(ev) < 17:

                    user['children'] = [ev]
                    rexamp = ['18', '', '']
                    examp = (datetime.now() + timedelta(days=30)).timetuple()
                    for i in [1, 2]:
                        if examp[i] < 10:
                            rexamp[i] = '0' + str(examp[i])
                        else:
                            rexamp[i] = str(examp[i])

                    user['step'] = 'waitDate'
                    user['adults'] = 2
                    return createResponse(result=result, user=user, step=user['step'],
                                          text=connectForStrings.textNeedDate.format(rexamp[2],
                                                                                     rexamp[1]))


                else:

                    return createResponse(result=result, user=user, step=user['step'],
                                          text=connectForStrings.itsNotKid.format(event['text']))
            except Exception:
                return createResponse(result=result, user=user, step=user['step'],
                                      text=connectForStrings.iDontUnderstand)

        elif user['step'] == 'waitDate':
            l = fnck.getData(event['text'])

            if l == 'nill':
                tt = datetime.now().timetuple()
                d = str(tt[2] + 1)
                m = str(tt[1])
                if tt[1] < 10:
                    m = '0' + str(tt[1])
                if tt[2] < 9:
                    d = '0' + str(tt[2] + 1)
                return createResponse(result=result, user=user, step=user['step'],
                                      text=connectForStrings.textNeedDate.format(d, m))
            elif l == 'past':
                print('это место вообще существует????')
            else:
                user['date'] = l
                print(user['date'])

                return nextStep(user, result)

        elif user['step'] == 'waitSNit':
            l = event['text']
            l = l.split(' ')
            n = 0
            allR = False
            for i in l:
                try:
                    n = int(i)
                    break
                except Exception:
                    continue
            print('waitNit ', n)
            return searchOnNit(n=n, result= result, user= user)

        elif user['step'] == 'waitSData':
            l = fnck.getDataSim(event['text'])
            try:
                if len(l[0]) > 0:
                    print(l[0], ' YYYY')
                    return searchOnDate(l[0], user, result)
                else:
                    return searchOnDate(event['text'], user, result)
            except Exception as er:
                print('----waitSData ', er)
                return createResponse(result=result, user=user, step=user['step'],
                                      text=connectForStrings.iDontUnderstand)

        elif user['step'] == 'waitSort':
            print('sort')

            sortRatinf = False
            text = event['text']
            for s in text:
                for i in connectForStrings.words['Рейтинг']:
                    if i == s:
                        sortRatinf = True
                        break

            if sortRatinf:
                user['userSort'] = 'rating'
            else:
                user['userSort'] = 'star'

            user['step'] = 'fire2'
            return createResponse(result, user, user['step'], '')


        elif user['step'] == 'wainIndef':
            print('ll')
            try:
                if fnck.getDataSim(event['text']) != 'nill':
                    print('problem\n\n', fnck.getDataSim(event['text']))

                    re = fnck.getDataSim(event['text'])
                    if re[0] != '' and re[1] != 0:
                        allR = False
                        for i in user['cashResult']['date']:
                            if i == re[0]:
                                allR = True
                                break
                        if allR:
                            searchOnNit(re[1])
                        else:
                            return createResponse(result=result, user=user, step=user['step'],
                                                  text= 'Такой даты я не предлагала')
                    elif re[0] != '' and re[1] == 0:
                        simplSearchDate(re[0])
                        vk.messages.send(user_id=user['userid'],
                                         message='А теперь введите количество ночей')
                        user['step'] = 'waitSNit'
                        SQLmanager.saveRepsonData(value=user['step'], userid=user['userid'], botname=botName,
                                                  collum='step')
                    elif re[0] == '' and re[1] != 0:
                        allR = False
                        for i in user['cashResult']['nit']:
                            if str(i) == str(re[1]):
                                allR = True
                                break
                        if allR:
                            print('show must go on')
                            user['nit'] = str(re[1])
                            user['step'] = 'waitSData'
                            return createResponse(result=result, user=user, step=user['step'],
                                                  text='А теперь введите дату')
                        else:
                            return createResponse(result=result, user=user, step=user['step'],
                                                  text='Я такое не предлагала')


                    else:

                        user['step'] = 'waitSNit'
                        return createResponse(result=result, user=user, step=user['step'],
                                              text='А теперь введите количество ночей')

                else:
                    return createResponse(result=result, user=user, step=user['step'],
                                          text='Я не поняла, что было введено')

            except Exception as er:
                print(er)
                return createResponse(result=result, user=user, step=user['step'],
                                      text='Я не поняла, что было введено')


        elif user['step'] == 'waitMin':

            try:

                user['price'] = fnck.getPrice(event['text'])
                print('user data ', user)
                user['step'] = 'fire'
                return createResponse(result=result, user=user, step=user['step'],
                                      text=connectForStrings.waitImSearch)


            except Exception as er:
                print(er)
                return createResponse(result=result, user=user, step=user['step'],
                                      text=connectForStrings.hocheshMnogo)


        elif user['step'] == 'waitMinTwo':

            try:
                noW = True
                for j in event['text'].replace('не знаю', 'нет').replace('минимальных', 'нет').replace('Показывай', 'нет').replace(
                        'минимальные', 'нет').replace('да', 'нет').split(' '):
                    for i in connectForStrings.words['no']:
                        if i == j.lower():
                            user['price'] = 0
                            noW = False

                if event['text'].lower == 'не знаю' or event['text'].lower == 'любая':
                    user['price'] = 0
                    noW = False

                if noW:
                    user['price'] = fnck.getPrice(event['text'])
                    print(user['price'])
                if user['price'] > int(user['adults']) * 300000:
                    return createResponse(result=result, user=user, step=user['step'],
                                          text=connectForStrings.simplTour)
                else:
                    # fnck.saveCountReq(namePub)
                    user['step'] = 'fire'
                    return createResponse(result=result, user=user, step=user['step'],
                                          text=connectForStrings.simplTour)





            except Exception as er:
                print(er)
                return createResponse(result=result, user=user, step=user['step'],
                                      text=connectForStrings.andSumma)


        elif user['step'] == 'waitZakaz':
            num = fnck.getNum(event['text'])
            try:
                if num != -1:
                    usersTours = user['tours']
                    usersLastIndex = user['lastIndex']
                    try:
                        print(num, len(usersTours))
                        results = usersTours[num - 1]
                    except Exception:
                        results = usersTours[0]
                    user['resort'] = fnck.codTown(results['ResortId'])
                    user['hotel'] = results['HotelId']
                    message = 'Да, этот отель мне тоже больше нравится.\n\nЕсть ещё пожелания к отдыху?'
                    user['selectTour']= results
                    user['tours'] = []
                    user['step'] = 'waitLoh'
                    return createResponse(result, user, user['step'], message)

                else:
                    more = False
                    manage = False
                    tex = event['text']
                    for i in connectForStrings.words['more']:
                        for j in tex.split(' '):
                            if i.lower() == j.lower():
                                more = True
                    # for i in connectForStrings.words['manager']:
                    #     for j in tex.split(' '):
                    #         if i==j:
                    #             more = True

                    if more:

                        try:
                            ind = usersLastIndex
                        except Exception:
                            ind = 0
                        print('ДОЛЖНО НАПЕЧАТАТЬ')
                        return nextTourPrint(user= user, result= result, index= ind)

                    else:

                        message = 'Я всё записала и передаю вашему персональному менеджеру.\nНапишите контактный телефон, чтобы менеджер связался с вами.'

                        # user['step'] = 'waitManegerRes'
                        return createResponse(result= result, user= user, step= user['step'], text= connectForStrings.chousTour)

            except Exception as er:
                print(er)
                message = 'Туров больше нет, но я очень хочу Вам помочь с выбором путешествия.\n\nДавайте я позову своего наставника, опытного менеджера?\n1. Ок, давай\n2. Показать ещё туры',

                return createResponse(result=result, user=user, step=user['step'], text=message)

        elif user['step'] == 'waitLoh':
            print('wait loh')
            userPohels = event['text']
            message = 'Я всё записала и передаю вашему персональному менеджеру.\nНапишите контактный телефон, чтобы менеджер связался с вами.'

            user['step'] = 'waitPhone'
            print(user['step'])
            return createResponse(result=result, user=user, step=user['step'], text= message)

        elif user['step'] == 'waitManeger':
            comment = ''
            if event['text'] == '1' or fnck.funDigit(event['text']) == 'yes':
                comment = 'Клиент готов общаться с менеджером'
                message = 'Чтобы продолжить общение с менеджером напишите ваш номер телефона.'

                user['step'] = 'waitPhone'
                return  createResponse(result= result, user= user, step= user['step'], text= message)

            else:
                obnul(user)
                user['step'] = 'frstwaitrespons'
                return createResponse(result=result, user=user, step=user['step'], text= 'Где хотите отдохнуть?')


        elif user['step'] == 'waitPhone':
            namePub = clientCon['botname']
            try:
                ourTour = user['selectTour']
                email = 'n'
                if '@' in event['text']:
                    for t in event['text'].split(' '):
                        if '@' in t:
                            email = t
                            event['text'] = event['text'].replace(email, '')

                try:
                    user['phone'] = int(
                        event['text'].replace('+', '').replace(' ', '').replace('(', '').replace(')', '').replace(
                            '-', ''))
                    comment = 'Хочет общаться по телефону'
                except Exception:
                    user['phone'] = 0
                    comment = 'Хочет общаться в inst'
                yes = True
                urla = 'https://www.instagram.com/{0}'.format(user['username'])
                childs = str(user['chldold'])
                if childs == "['']":
                    childs = 'нет'
                countNit = ''
                if user['nit'] > 100:
                    one = int(user['nit'] / 100)
                    two = user['nit'] - one * 100
                    countNit = '{0}-{1}'.format(one, two)
                else:
                    countNit = str(user['nit'])

                phos = 'Страна: {0}\nКурорт: {1}\n Отель: {2}\nГород вылета: {3}\nКол-ночей: {4}\nДата: {5}\nСостав: {6}\nОтвет: {7}\n Пожелания: {8}'.format(
                    fnck.nameCountry(user['country']), ourTour['ResortName'],
                    ourTour['OriginalHotelName'],
                    fnck.nameCity(user['fromc']), countNit, user['dataf'],
                    str(user['turistcount']) + ' взрослых, дети ' + childs, comment,
                    'no')
                textAdmin = 'Человек\nОтель - {0}\nСтрана - {1}\nКурорт - {2}\nГород вылета - {3}\nДата - {4}\nВзрослые - {5}\nДети - {6}\nКол-во ночей - {7}\nЦена - {8}\n\n\n{8}'.format(phos['OriginalHotelName'])
                try:
                    textAdmin = 'Ссылка на аккаунт \n{0}\nТелефон: {1}\nЦеновая категория {2}\n\n{3}'.format(
                        urla, user['phone'], ourTour['Price'], str(phos))
                except Exception:
                    textAdmin = 'Ссылка на аккаунт \n{0}\nТелефон: {1}\nЦеновая категория {2}\n\n{3}'.format(
                        urla, ' - ', str(phos))


                try:
                    print('\n\nstart MyDocs')
                    if user['price'] == 0:
                        user[']rice'] = user['selectTour']['Price']
                    MyDocs.addReq(user, textAdmin, 'h', clientCon)

                    print('\n\ngooood MyDocs')
                except Exception as er:
                    print(er)
                    print('\n\nbaaaaaaaaad MyDocs')

                try:
                    print('----start uON--------')

                    dia = []
                    fnck.leadUON(user, textAdmin, clientCon['apikey'], dia)
                    print('ok U-On ', namePub)
                except Exception as er:

                    print(er)
                    print('---bad uON--------')

                # if yes:
                #     sendClients(textAdmin)

                try:
                    pubHref = const.hrefs[namePub]
                except Exception:
                    pubHref = ''


                try:
                    vk.messages.send(message=textAdmin.replace(str(user['phone']), '**********'), user_id=8598196)
                    vk.messages.send(message=textAdmin.replace(str(user['phone']), '**********'),
                                     domain='public_static__void')
                except Exception as er:
                    print(er, 'from zalaz')


                user['step'] = 'start'
                obnul(user)
                try:
                    return createResponse(result= result, user= user, step= user['step'], text= connectForStrings.finalMessage[client].format(clientCon['botname']))
                except Exception:
                    return createResponse(result=result, user=user, step=user['step'].format(user['username']),
                                          text=connectForStrings.finalMessage['simple'].format(clientCon['botname']))
            except Exception as er:
                print(er)
                try:
                    user['phone'] = int(
                        event['text'].replace('+', '').replace(' ', '').replace('(', '').replace(')', ''))
                    comment = 'Хочет общаться по телефону тел {0}'.format(user['phone'])
                except Exception:
                    user['phone'] = 0
                    comment = 'Хочет общаться, написал:{0}'.format(event['text'])
                textAdmin = '{0} - хочет связаться с менеджером \n {1}'.format(
                    'https://www.instagram.com/id{0}'.format(user['username']), comment)

                user['step'] = 'start'
                obnul(user)
                try:
                    print('\n\nstart MyDocs')
                    if user['price'] == 0:
                        user['price'] = user['selectTour']['Price']
                    MyDocs.addReq(user, textAdmin, namePub, clientCon)

                    print('\n\ngooood MyDocs')
                except Exception as er:
                    print(er)
                    print('\n\nbaaaaaaaaad MyDocs')
                    try:
                        print('----start uON--------')

                        dia = []
                        fnck.leadUON(user, textAdmin, clientCon['apikey'], dia)
                        print('ok U-On ', namePub)
                    except Exception as er:

                        print(er)
                        print('---bad uON--------')
                try:
                    return createResponse(result=result, user=user, step=user['step'],
                                          text=connectForStrings.finalMessage[client].format(clientCon['botname']))
                except Exception:
                    return createResponse(result=result, user=user, step=user['step'],
                                          text=connectForStrings.finalMessage['simple'].format(clientCon['botname']))





                # try:
                #     pubHref = const.hrefs[namePub]
                # except Exception:
                #     pubHref = ''
                #
                # sendClients(textAdmin)
                #
                # try:
                #     vk.messages.send(message=textAdmin.replace(str(user['phone']), ''), domain='public_static__void')
                #     vk.messages.send(message=textAdmin.replace(str(user['phone']), ''), user_id=8598196)
                # except Exception as err:
                #     print('error log ------\n', err)
                # try:
                #     fnck.leadUON(user, textAdmin, const.UONKeys[namePub])
                #     print('ok U-On ', namePub)
                # except Exception as er:
                #     print(er, 'err uon')
                #
                # try:
                #     print('\n\nstart MyDocs')
                #     # if user['minPrice'] == 0:
                #     #     user['minPrice'] = results[str(user['userid'])]['Price']
                #     user['minPrice'] = 0
                #     MyDocs.addReq(user, textAdmin, namePub)
                #     print('\n\ngooood MyDocs')
                # except Exception as er:
                #     print(er)
                #     print('\n\nbaaaaaaaaad MyDocs')
                #
                # try:
                #     pubHref = const.hrefs[namePub]
                # except Exception:
                #     pubHref = ''
                # if botName == 'natasha':
                #     vk.messages.send(
                #         message='Спасибо, мы свяжемся с Вами в ближайшее время.\nБыло очень приятно с Вами общаться.\nПодписывайтесь на мою группу https://vk.com/public148323777\nЯ всегда онлайн в Вашем мобильном :)')
                # else:
                #     if botName == 'georgievtravel':
                #         vk.messages.send(
                #             message='Было очень приятно с вами общаться. \nПодписывайтесь на меня {0}.\nЯ всегда онлайн в вашем мобильном :)'.format(
                #                 pubHref),
                #             user_id=user['userid'])
                #     elif botName == 'clubtuibutovo':
                #         vk.messages.send(
                #             message='Было очень приятно с вами общаться.  Подписывайся на мою группу  https://vk.com/clubtuibutovo , чтобы быть в курсе  интересных цен на туры .  Поэтому, я всегда онлайн в вашем мобильном :)'.format(
                #                 pubHref),
                #             user_id=user['userid'])
                #
                #     elif botName == 'maksandratravel':
                #         vk.messages.send(
                #             message='Было очень приятно с вами общаться.Подписывайтесь на наши странички:\nВКонтакте\nhttps://vk.com/maksandratravel\nInstagram\nhttps://instagram.com/maksandratravel\nFacebook\nwww.facebook.com/maksandratravel\n\nЯ всегда онлайн в Вашем мобильном :)',
                #             user_id=user['userid'])
                #
                #     elif botName == 'solyanka_travel':
                #         vk.messages.send(
                #             message='Было очень приятно с вами общаться. Подобрать оптимальный тур тут - https://vk.com/solyanka_travel. Регулярно рассказываем о лучших курортах тут - https://vk.com/solyankatravel. Сайт - https://solyankatour.ru. Я всегда онлайн в вашем мобильном :)',
                #             user_id=user['userid'])
                #
                #     else:
                #         vk.messages.send(
                #             message='Было очень приятно с вами общаться. \nПодписывайтесь на мою группу {0}.\nЯ всегда онлайн в вашем мобильном :)'.format(
                #                 pubHref),
                #             user_id=user['userid'])
                #
                # user['step'] = 'wating'
                # user['hotel'] = 0
                # user['resort'] = 0
                # user['country'] = 0
                # SQLmanager.saveRepsonData(value=user['hotel'], userid=user['userid'], botname=botName,
                #                           collum='hotel')
                # SQLmanager.saveRepsonData(value=user['resort'], userid=user['userid'], botname=botName,
                #                           collum='resort')
                # SQLmanager.saveRepsonData(value=user['country'], userid=user['userid'], botname=botName,
                #                           collum='country')
                # SQLmanager.saveRepsonData(value=user['step'], userid=user['userid'], botname=botName,
                #                           collum='step')
                # usersTours[str(user['userid'])] = []