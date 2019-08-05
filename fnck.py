from lxml import etree
from lxml import html
import time
import json
from lxml.html import parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import soap
import time
from datetime import datetime, date, timedelta
import connectForStrings
from threading import Thread
hotels = []


def strToInt(st):
    return int(st)

def dval(str):
    i = 0
    words = []
    word = ''
    while i < len(str):
        if i == len(str) - 1:
            word = word + str[i]
            word = word.capitalize()
            words.append(word)
            break
        if str[i] == ' ':
            word=word.capitalize()
            words.append(word)
            word = ''
            i = i + 1
        word = word + str[i]
        i = i + 1
    return words

def fhot(user, hotel):

    result=0
    i=0
    duser=dval(user)
    dhotel=dval(hotel)
    i=0
    j=0

    while i<len(duser):
        j=0
        while j<len(dhotel):
            if distance(duser[i],dhotel[j])<2:
                result=result+1
            j=j+1
        i=i+1
    # print(dhotel)

    return result

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def funDigit(text):

    if text.lower() == 'мск':
        return 'москва'
    if text.lower() == 'нск':
        return 'новосибирск'

    for k, w in connectForStrings.words.items():

        for sw in w:

            if fhot(sw.lower(),text.lower())>0:
                return k

    return text




def checkCity(ct):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/departureCities/departureCity')

    for k, w in connectForStrings.words.items():

        for sw in w:

            if fhot(sw.lower(),ct.lower()):
                return 1

    f=0
    for c in cts:

        name = c.get('name').lower()
        ct=ct.lower()
        if fhot(ct, name) > 0:
            f = 1
        # if name == ct:
        #
        #     f=1
    if f==0:
        return 0
    else:
        return 1

def codCity(name):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/departureCities/departureCity')
    a = name.replace('-',' ').split(' ')
    str = ''
    u= ''

    for i in a:
        u=i.capitalize()
        str = str + u

    cod = 0
    # if name=='нск':
    #     name='Новосибирск'
    # if name=='мск':
    #     name='Москва'
    # if name=='спб':
    #     name='Санкт-Петербург'.split('-')


    name = name.capitalize()
    for k, w in connectForStrings.words.items():

        for sw in w:

            if fhot(sw.lower(),name.lower())>0:
                str = k
    # print(str)
    for ct in cts:
        # print(ct.get('name'))
        if fhot(ct.get('name').replace(' ', '').replace('-', ''),str.replace(' ', '').replace('-', '')) > 0:
            cod = ct.get('id')
        # if ct.get('name').replace(' ', '').replace('-', '')==str.replace(' ', '').replace('-', ''):
        #     cod=ct.get('id')
    print(cod)
    return cod

def codCountry(name):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/countries/country')
    cod = 0

    for ct in cts:

        if ct.get('name').lower()==name.lower():
            cod=ct.get('id')

    return cod

def nameCountry(cod):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/countries/country')
    name = ''
    for ct in cts:

        if int(ct.get('id'))==int(cod):
            name=ct.get('name')

    return name

def nameTown(cod):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/resorts/resort')
    name = ''
    for ct in cts:
        if ct.get('id')==str(cod):
            name=ct.get('name')

    return name

def nameHotel(cod):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/hotels/hotel')
    name = ''
    for ct in cts:
        if ct.get('id')==str(cod):
            name=ct.get('name')

    return name

def nameCity(cod):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/departureCities/departureCity')
    name = ''
    for ct in cts:
        if ct.get('id')==str(cod):
            name=ct.get('name')

    return name

def codTown(name):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/resorts/resort')
    try:
        cod = 0
        for ct in cts:
            if ct.get('name')==str(name):
                cod=ct.get('id')

        return cod
    except Exception:
        return 0

def checkResort(resort):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/resorts/resort')

    check = 0
    for ct in cts:
        if ct.get('name') == resort.capitalize():
            check = 1

    return check

def checkCountry(country):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/countries/country')

    a = country.replace('-', ' ').split(' ')
    str = ''
    u = ''
    for i in a:
        u = i.capitalize()
        str = str + u

    check = 0
    for ct in cts:
        if ct.get('name').replace(' ', '').replace('-', '').lower() == str.replace(' ', '').replace('-', '').lower():
            check = 1

    if country == 'ОАЭ':
        check = 1

    return check


def mail(em, txt, fromY):
    me = 'tourbot@more-r.ru'
    lena = em
    smtp_server = 'smtp.beget.ru'
    # msg = MIMEMultipart('alternative')
    htm = """\
    <html>
        <body>
        <p><font size="10" color="red">hello lena</font></p>
        </body>

    </html>
    """
    msg=MIMEText(txt,"","utf-8")
    msg['Subject'] = 'Заявка из {0} бота'.format(fromY)
    msg['From'] = me
    msg['To'] = lena
    # h = MIMEText(htm, 'html')
    # msg.attach(h)
    s = smtplib.SMTP(smtp_server)
    # s.set_debuglevel(1)
    s.starttls()
    s.login('tourbot@more-r.ru', 'Z19i08ZA')
    s.sendmail(me, [lena], msg.as_string())
    s.quit()

def distance(a, b):
    a = a.replace(' ', '')
    b = b.replace(' ', '')

    if len(a) > len(b):
        dis = len(a) - len(b)
        i = 0
        j=0
        while i < len(b):
            if b[j]==' ':
                j=j+1
            if a[i] != b[j]:
                dis = dis + 1
            i = i + 1
            j=j+1
    else:

        dis = len(b) - len(a)
        i = 0
        j=0
        while i < len(a):
            if b[j]==' ':

                j=j+1
            if a[i] != b[j]:
                dis = dis + 1
            i = i + 1
            j=j+1
    return dis

def devages(a):
    ags=[]
    a= a.replace(' ', '')
    a=a+','
    b=''
    for i in a:
        if i==',':
            ags.append(int(b))
            b=''
        else:
            b=b+i
    return ags

def devspace(n):
    a=str(int(n/1000))
    b=str(n-int(n/1000)*1000)
    if int(b)<100:
        b='0'+b
    return a +' '+b

def parsing (stri, pos):

    dict={}
    i=pos+1
    vr=0
    list = ''
    varbl = ''

    srr = 0
    l = i
    while 1:

        if stri[l] == '{':
            srr = srr + 1
        if stri[l] == '}':
            if srr  == 0:
                break
            if srr != 0:
                srr = srr - 1
        l += 1

    while 1:
        if i==l:

            try:
                if float(varbl) == float(int(float(varbl))):
                    dict[list] = int(varbl)

                else:
                    dict[list] = float(varbl)
            except Exception:

                dict[list]=varbl
            # print(i)

            break
        if stri[i]=='{':
            j = i + 1
            k = 0
            sr = 0
            while 1:
                if stri[j] == '{':
                    sr = sr + 1
                if stri[j] == '}':
                    if sr == 0:
                        break
                    if sr!= 0:
                        sr = sr - 1
                j += 1
                k = k + 1

            u = parsing(stri, i)

            if len(str(u)) == 4:
                u = []

            if stri[j + 1] == ',':
                i = j + 1
                varbl = u
            if stri[j + 1] == '}':
                dict[list] = u

                break
        if stri[i]=='[':
            j = i + 1
            k = 0
            sr = 0
            while 1:
                if stri[j] == '[':
                    sr = sr + 1
                if stri[j] == ']':
                    if sr == 0:
                        break
                    if sr!= 0:
                        sr = sr - 1
                j += 1
                k = k + 1

            u=getAr(stri, i)

            if len(str(u))==4:
                u=[]

            if stri[j+1]==',':
                i=j+1
                varbl=u
            if stri[j + 1] == '}':
                dict[list] = u
                break

        if stri[i]==',':
            try:
                if float(varbl) == float(int(float(varbl))):
                    dict[list] = int(varbl)

                else:
                    dict[list] = float(varbl)
            except Exception:

                dict[list]=varbl
            list=''
            varbl=''
            vr=0
            i=i+1
        if stri[i]==':':
            vr=1
            i=i+1
        elif vr==0:
            list=list+stri[i]
            i=i+1
        elif vr==1:
            varbl=varbl+stri[i]
            i=i+1

    return dict

def getAr(stri, pos):

    arr=[]
    i=pos+1
    arg=''

    srr=0
    l=i
    while 1:

        if stri[l] == '[':
            srr = srr + 1
        if stri[l] == ']':
            if srr == 0:
                break
            if srr != 0:
                srr = srr - 1
        l += 1

    while 1:
        if i==l:

            try:
                if float(arg) == float(int(float(arg))):
                    arr.append(int(arg))

                else:
                    arr.append(float(arg))
            except Exception:

                arr.append(arg)
            # print(arr)
            break
        if stri[i]=='[':
            j=i+1
            k=0
            sr=0
            while 1:
                if stri[j]=='[':
                    sr=sr+1
                if stri[j]==']':
                    if sr==0:
                        break
                    if sr!=0:
                        sr=sr-1
                j+=1
                k=k+1
            u=getAr(stri,i)

            if len(str(u))==4:
                u=[]


            if stri[j+1]==',':
                i=j+1
                arg=u
            if stri[j+1]==']':
                arr.append(u)

                break


        if stri[i]=='{':
            j = i + 1
            k = 0
            sr = 0
            while 1:
                if stri[j] == '{':
                    sr = sr + 1
                if stri[j] == '}':
                    if sr == 0:
                        break
                    if sr != 0:
                        sr = sr - 1
                j += 1
                k = k + 1
            u = parsing(stri, i)

            if len(str(u)) == 4:
                u = []

            if stri[j + 1] == ',':
                i = j + 1
                arg = u
            if stri[j+1] == ']':
                arr.append(u)

                break


        elif stri[i]==',':
            try:
                if float(arg) == float(int(float(arg))):
                    arr.append(int(arg))

                else:
                    arr.append(float(arg))
            except Exception:

                arr.append(arg)
            arg=''
            i=i+1
        else:
            arg=arg+stri[i]
            i=i+1

    return arr

def getDiscript(url):
    discr = ''
    response = requests.get(url)
    parsed_body = html.fromstring(response.text)

    scriptText = parsed_body.xpath('//script/text()')
    if not scriptText:
        print("Found No Text")
        return 'null'
    jso = scriptText[2].replace('window.__INITIAL_STATE__ = ','')

    discr = parsing(jso.replace('"',''), 0)['pageModel']['hotelDetails']['description']

    return discr

def getPhotoTitle(url):
    photoUrl = ''
    response = requests.get(url)
    parsed_body = html.fromstring(response.text)



    # print(response.text.index('carousel-photo-0'))
    # print(images)
    scriptText = parsed_body.xpath('//div//img/@src')
    print(scriptText)
    # if not scriptText:
    #     print("Found No Images")
    #     return 'null'



def itsHotel(text, hotels):
    result = []
    for h in hotels:
        if fhot(text, h['nameHotel']) >= len(dval(text)) and len(dval(h['nameHotel'])) < (len(dval(text)) + 5):
            result.append([h['nameHotel'], h['idHotel'], h['country'], nameTown(h['resortId']), h['star']])

    return result


def itsResort(text):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/resorts/resort')
    resorts = []
    text = funDigit(text)
    text = text.lower()
    if text == 'гоа':
        return [['Гоа', codCountry('Индия')]]
    for h in cts:
        if fhot(text, h.get('name').lower()) >= len(dval(text)) and len(dval(h.get('name').lower())) < (len(dval(text)) + 3):
            resorts.append([h.get('name'), h.get('countryId')])
    return resorts

def checkCountryTwo(text):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/countries/country')
    text = text.lower()
    if funDigit(text) != text:
        text = funDigit(text)

    if text.lower() == 'тай':
        return 'Тайланд'

    if text.lower() == 'бали':
        return 'Индонезия'

    for c in cts:

        if fhot(text.replace(' ', ''), c.get('name').lower().replace(' ','')) >= 1:
            return c.get('name')

    if text == 'оаэ':
        return 'ОАЭ'
    if text.lower() == 'бали':
        return 'Бали'

    return 0


def relaxRespons(text, hotels):
    result ={}
    hotel = itsHotel(text, hotels)
    req = text.replace(',',' ').replace('.',' ').replace('  ',' ').split(' ')

    for i in req:
        if i.lower() == 'море':
            return ['sea']
    for i in req:
        print(i, 'words')
        if checkCountryTwo(i) != 0 and len(i) > 3 or i.lower() == 'тай':
            print(checkCountryTwo(i), '--------check Country')
            return ['country', checkCountryTwo(i)]
    for i in req:
        if itsResort(i) != [] and len(i) > 2:
            return ['resort', itsResort(i)]

    if hotel != []:
        return ['hotel', hotel]
    else:
        return []



def getPrice(text):
    text = text.replace(' ', '').replace('.', '').replace(',','')
    workT = ''
    for i in text:
        try:
            if i != '-':
                f = int(i)
                workT += i
            else:
                workT += i
        except Exception:
            continue
    text = workT

    arr = text.split('-')
    g = -1
    all = []

    for i in arr:
        try:
            g = int(i)
            all.append(g)
        except Exception:
            continue

    print('det price', arr)



    result = 0
    for i in all:
        result += i
    try:
        result = int(result/len(all))
    except Exception:
        result = 0

    if result < 1000:
        result *= 1000

    return result

def countryForUon(name, key):
    f = requests.get('https://api.u-on.ru/{0}/countries.json'.format(key))
    idR = json.loads(f.text)
    result = ''
    for i in idR['records']:
        if i['name'] == name:
            return str(i['id'])
    try:
        url = 'https://api.u-on.ru/{0}/country/create.json'.format(key)
        data = {'name': name, 'name_en': translate(name)}
        res = requests.post(url, data=data)
        return str(json.loads(res.text)['id'])
    except Exception as er:
        print('error from countryForUpu:\n', er)
        return '1'

def leadUON(user, text, key, histDia = [], email= 'n'):
    url = 'https://api.u-on.ru/{0}/lead/create.json'.format(key)
    try:
        data = {'r_id_internal': 'VK заявка от {0} {1}'.format(user['last_name'],  user['first_name']), 'source': 'vk_bot', 'u_surname': user['last_name'], 'u_name': user['first_name'],
                'u_phone': user['phone'], 'u_note': text, 'date_from': user['dataf'], 'nights_from': str(user['nit']), 'countries': countryForUon(nameCountry(user['country']), key), 'budget': user['minPrice']}
    except Exception:
        data = {'r_id_internal': 'VK заявка от {0} {1}'.format(user['last_name'], user['first_name']),
                'source': 'vk_bot', 'u_surname': user['last_name'], 'u_name': user['first_name'],
                'u_phone': user['phone'], 'u_note': text}
    if email != 'n':
        data['u_email'] = email
    res = requests.post(url, data=data)
    print(res.text)
    idR = json.loads(res.text)['id']
    print(idR)
    if len(histDia) > 0:
        addComUon(key= key, dialogs= histDia, r_id=idR)


class UON(Thread):

    def __init__(self, data, dialogs, key):
        Thread.__init__(self)
        self.data = data
        self.dialogs = dialogs
        self.key = key

    def client(self):
        url = 'https://api.u-on.ru/zv59ViPp9vChB52FIQh6/service/create.json'

        res = requests.post(url, data= self.data)
        print(res.text)
        if json.loads(res.text)['result'] != 200:
            time.sleep(10)
            self.client()
        else:
            if len(self.dialogs) > 0:
                addComUon(key= self.key, dialogs= self.dialogs, r_id= json.loads(res.text)['id'])

    def run(self):
        time.sleep(15)
        self.client()

def postUOn(user, price, key = 'zv59ViPp9vChB52FIQh6', histDia = []):

    r = 'zv59ViPp9vChB52FIQh6'
    url = 'https://api.u-on.ru/{0}/request/create.json'.format(key)
    data = {'r_id_internal': 'VK заявка от {0} {1}'.format(user['last_name'],  user['first_name']), 'source': 'vk', 'price': str(price), 'u_surname': user['last_name'], 'u_name': user['first_name'], 'u_phone_mobile': str(user['phone'])}

    res = requests.post(url, data=data)
    idR = json.loads(res.text)['id']
    print(idR)

    url = 'https://api.u-on.ru/{0}/service/create.json'.format(key)
    print(nameCountry(user['country']))
    data = {'r_id': idR, 'type_id': 1, 'country': nameCountry(user['country']) , 'city': nameTown(user['resort']), 'hotel': nameHotel(user['hotel']) , 'nights_from': user['nit'], 'date_begin': user['dataf'],
            'date_to': user['dataf'], 'tourists_baby_count': user['turistcount'], 'tourists_child_count': len(user['chldold'])}
    ss = UON(data= data, key= key, dialogs= histDia)
    ss.start()



def postMethod(data, met, key):
    s = requests.Session()
    url = 'https://api.u-on.ru/{0}/'.format(key) + met
    reault = s.post(url= url, data= data)
    return json.loads(reault.text)

def rete(key, id, text):
    data= {
        'r_id': id,
        'type_id': 2,
        'text': text,
        'datetime': str(datetime.today() + timedelta(hours= 3))
    }
    return postMethod(met= 'request-action/create.json', key= key, data= data)

def addComUon(key, dialogs, r_id):
    print(dialogs)
    time.sleep(13)
    for i in dialogs:
        try:
            print(rete(key= key, id= r_id, text= i))
        except Exception as er:
            print('--')
            print(er)
    pass

def checkInt(text):
    for i in text:
        if i >= '0' and i <= '9':
            return i
    return text

def funForData(text):
    for k, w in connectForStrings.words.items():
        try:
            a= int(k)
            for sw in w:
                if fhot(sw.lower(), text.lower()) > 0:
                    return k
        except Exception:
            continue

    return text

def getData(text):
    print('-------data---------')
    result = ''
    try:
        mm = text
        dotCheck = 0
        mm = mm.replace(',', ' . ').replace(' ',' + ').replace('.', ' . ').replace(' c ', ' ').replace('-', ' + ').split(' ')
        print(mm, '555')
        m = []
        for j in mm:
            try:
                if j == '+':
                    dotCheck = 0

                if dotCheck == 3:
                    dotCheck = 0
                    continue
                if j == '.':
                    dotCheck += 1


                if j.lower() == 'начало' or j.lower() == 'начале':
                    m.append('5')
                elif j.lower() == 'конец' or j.lower() == 'конце':
                    m.append('23')
                j = funForData(j)
                a = int(j)
                if a>0 and a<32:
                    m.append(j)
            except Exception:
                continue
        past = False

        print('arr data now ', m)


        if m[0].lower() == 'начало':
            m[0] = '5'
        elif m[0].lower() == 'конец':
            m[0] = '23'
        else:
            m[0] = funDigit(str(m[0]))
        m[1] = funDigit(str(m[1]))

        i = 0
        while i < len(m):
            if len(m[i]) == 1:
                m[i] = '0' + m[i]
            i += 1

        print(m)

        y = datetime.now().timetuple()[0]
        print(datetime.now().timetuple())
        if strToInt(m[1]) < datetime.now().timetuple()[1]:
            y = y + 1



        if len(m) == 2:
            if int(m[0])>31 or int(m[1])>12:
                return 'nill'
            result = m[0] + '.' + m[1] + '.' + str(y)
            tm = [m[0], m[1]]
        elif len(m) == 3:
            if strToInt(m[2]) < datetime.now().timetuple()[1]:
                y = y + 1
            tm = [m[0], m[2], m[1], m[2]]
            result ='{0}.{1}.{2}/{3}.{4}.{5}'.format(m[0],m[2],y,m[1],m[2],y)
        elif len(m) == 4:
            tmn = datetime.now().timetuple()[1]

            tm = [m[0], m[1], m[2], m[3]]
            result ='{0}.{1}.{2}/{3}.{4}.{5}'.format(m[0],m[1],y if int(m[1]) >= int(tmn) else y+1,m[2],m[3],y if int(m[3]) >= int(tmn) else y+1)
        print(result)
        # if (int(tm[0]) < datetime.now().timetuple()[2] and int(tm[1]) == datetime.now().timetuple()[1]) or int(tm[1]) < datetime.now().timetuple()[1]:
        #     past = True
        #     return 'past'

    except Exception as er:
        print(er)
        result = 'nill'
    return result

def getDataSim(text):
    arr = text.replace('.', ' ').split(' ')
    itw = []
    y = datetime.now().timetuple()[0]

    for i in arr:
        try:
            itw.append(int(funDigit(i)))
        except Exception:
            continue
    if len(itw)>1:
        if itw[0]<10:
            d = '0'+ str(itw[0])
        else:
            d = str(itw[0])
        if itw[1] < 10:
            m = '0' + str(itw[1])
        else:
            m = str(itw[1])

    if len(itw) == 2:
        return ['{0}.{1}.{2}'.format(d, m, y), 0]
    elif len(itw) == 3:
        return ['{0}.{1}.{2}'.format(d, m, y), itw[2]]
    elif len(itw) == 1:
        return ['' , itw[0]]
    return 'nill'

def getNum(text):
    for i in text.split(' '):
        try:
            return int(i)
        except Exception:
            continue
    return -1


def butyPrice(price):
    frst = int(price/1000)
    scrst = price - frst*1000
    if scrst < 100:
        if scrst < 10:
            scrst = '00'+str(scrst)
        else:
            scrst = '0' + str(scrst)
    return '{0} {1}'.format(frst, scrst)

def butyDate(data):
    a = data.split('.')
    mouns = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля','августа', 'сентября', 'октября', 'ноября', 'декабря']
    day = a[0]
    mou = mouns[int(a[1])-1]
    return '{0} {1}'.format(day, mou)


def resortsInfo(country):
    print('resortInfo ', country)
    f = open('Resort/Resorst.txt', 'r', encoding='utf-8')
    ff = f.read()

    arr = []
    j = 0
    for i in ff.split('\n'):
        if j > 2:
            arr.append(i.split('\t'))
        j += 1

    result = []

    for i in arr:
        if i[0] == country:
            a = {}
            a['resort'] = i[1]
            a['discript'] = i[2]
            a['img'] = i[3]
            result.append(a)

    f.close()
    return result

def likeResort(res, country):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/resorts/resort')
    resorts = []
    text = res.lower()


    for h in cts:
        if int(h.get('countryId')) == int(country):
            print(h.get('countryId'), country, h.get('name'))
        if text == h.get('name').lower() and int(h.get('countryId')) == int(country):
            return h.get('name')

    for h in cts:

        if fhot(text, h.get('name').lower()) >= 1 and int(h.get('countryId')) == int(country):
            return h.get('name')


def removeRepit(text):
    ar = text.split(' ')
    at = ar
    i = 0
    while i<len(ar):
        j=0
        while j<len(at):
            if ar[i] == at[j] and i != j:
                text = text.replace(ar[i], '')
            j += 1
        i += 1

    return text

def translate(name):

    # Заменяем пробелы и преобразуем строку к нижнему регистру
    name = name.replace(' ' ,'-').lower()

    #
    transtable = (
        ## Большие буквы
        (u"Щ", u"Sch"),
        (u"Щ", u"SCH"),
        # two-symbol
        (u"Ё", u"Yo"),
        (u"Ё", u"YO"),
        (u"Ж", u"Zh"),
        (u"Ж", u"ZH"),
        (u"Ц", u"Ts"),
        (u"Ц", u"TS"),
        (u"Ч", u"Ch"),
        (u"Ч", u"CH"),
        (u"Ш", u"Sh"),
        (u"Ш", u"SH"),
        (u"Ы", u"Yi"),
        (u"Ы", u"YI"),
        (u"Ю", u"Yu"),
        (u"Ю", u"YU"),
        (u"Я", u"Ya"),
        (u"Я", u"YA"),
        # one-symbol
        (u"А", u"A"),
        (u"Б", u"B"),
        (u"В", u"V"),
        (u"Г", u"G"),
        (u"Д", u"D"),
        (u"Е", u"E"),
        (u"З", u"Z"),
        (u"И", u"I"),
        (u"Й", u"J"),
        (u"К", u"K"),
        (u"Л", u"L"),
        (u"М", u"M"),
        (u"Н", u"N"),
        (u"О", u"O"),
        (u"П", u"P"),
        (u"Р", u"R"),
        (u"С", u"S"),
        (u"Т", u"T"),
        (u"У", u"U"),
        (u"Ф", u"F"),
        (u"Х", u"H"),
        (u"Э", u"E"),
        (u"Ъ", u"`"),
        (u"Ь", u"'"),
        ## Маленькие буквы
        # three-symbols
        (u"щ", u"sch"),
        # two-symbols
        (u"ё", u"yo"),
        (u"ж", u"zh"),
        (u"ц", u"ts"),
        (u"ч", u"ch"),
        (u"ш", u"sh"),
        (u"ы", u"yi"),
        (u"ю", u"yu"),
        (u"я", u"ya"),
        # one-symbol
        (u"а", u"a"),
        (u"б", u"b"),
        (u"в", u"v"),
        (u"г", u"g"),
        (u"д", u"d"),
        (u"е", u"e"),
        (u"з", u"z"),
        (u"и", u"i"),
        (u"й", u"j"),
        (u"к", u"k"),
        (u"л", u"l"),
        (u"м", u"m"),
        (u"н", u"n"),
        (u"о", u"o"),
        (u"п", u"p"),
        (u"р", u"r"),
        (u"с", u"s"),
        (u"т", u"t"),
        (u"у", u"u"),
        (u"ф", u"f"),
        (u"х", u"h"),
        (u"э", u"e"),
    )
    # перебираем символы в таблице и заменяем
    for symb_in, symb_out in transtable:
        name = name.replace(symb_in, symb_out)
    # возвращаем переменную
    return name

def getListHotels():
    result =[]
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/hotels/hotel')

    for h in cts:
        a = {
                'nameHotel': h.get('name'),
                'idHotel': h.get('id')
                # 'country': h.get()
        }
        result.append(a)
    return result



def checkResortFats(t):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/resorts/resort')
    resorts = []
    text = t.lower()
    if len(t)>3:
        for h in cts:
            if fhot(h.get('name').lower(),text) == 1:
                return [h.get('id'), h.get('countryId')]
    return []

def checkResortHz(t):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/resorts/resort')
    resorts = []
    text = t.lower()
    print('resort sc text', t)
    if text == 'сочи':
        return [1361 ,150]
    if len(t) > 2:
        for h in cts:
            for y in h.get('name').split(' '):
                if y.lower() == text:
                    return [h.get('id'), h.get('countryId')]
    return []

def deNit(nit):
    if nit>100:
        f = int(nit/100)
        s = nit - f*100
        return '{0}-{1}'.format(f, s)
    else:
        return str(nit)

def getStarHot(hotel):
    result = []
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/hotels/hotel')
    st = ['1*', '2*', '3*', '4*', '5*', 'Apts']
    for h in cts:
        if str(hotel) == str(h.get('id')):
            try:
                return st[int(h.get('starId')) - 400]
            except Exception:
                return ''
    return ''

def writeFile(name, text, act):
    fee = open(name, act, encoding='utf-8')
    fee.write(text)
    fee.close()

def openFile(name):
    f = open(name, 'r', encoding='utf-8')
    ff = f.read()
    f.close()
    return ff


def fastResort(text):
    tree = etree.parse('Dictionaries.xml')
    cts = tree.xpath('/dictionaries/resorts/resort')
    resorts = []
    result = []
    text = funDigit(text)
    text = text.lower()
    if text == 'гоа':
        return [['Гоа', codCountry('Индия')]]
    for h in cts:
        for i in dval(h.get('name')):
            if fhot(text, h.get('name').lower())==1 and len(text)>3:
                print(text, h.get('name'), fhot(text, h.get('name').lower()))
                result = [h.get('id'), nameCountry(h.get('countryId'))]

    return result


def creatNort(text, hotels):
    result = {'country': 0, 'resort': 0, 'hotels': itsHotel(text, hotels)}

    req = text.replace(',', ' ').replace('.', ' ').replace('  ', ' ').replace('день', ' ').split(' ')

    ft = datetime.now()
    print(text, ' input text')
    for i in req:
        if checkCountryTwo(i) != 0 and len(i) > 3 or i.lower() == 'тай' or i.lower() == 'оаэ':
            if i.lower() != 'бали':
                result['country'] = codCountry(checkCountryTwo(i))
                req[req.index(i)] = 'n'
    print('delta= ', (datetime.now() -ft).seconds)
    print(result)
    ft = datetime.now()
    for i in req:
        try:
            if req[req.index(i) - 1].lower() != 'из':
                if len(checkResortHz(i)) != 0:
                    result['resort'] = checkResortHz(i)[0]
                    if result['country'] == 0:
                        result['country'] = (checkResortHz(i)[1])
        except Exception:
            if len(checkResortHz(i)) != 0:
                result['resort'] = nameTown(checkResortHz(i)[0])
                if result['country'] == 0:
                    result['country'] = (checkResortHz(i)[1])
    print('delta1= ', (datetime.now() - ft).seconds)
    ft = datetime.now()

    # if result['resort'] == 0:
    #     for i in req:
    #         try:
    #             if req[req.index(i) - 1].lower() != 'из':
    #                 a = fastResort(i)
    #                 if len(a) > 0:
    #                     result['resort'] = a[0]
    #                     result['country'] = a[1]
    #         except Exception:
    #             da = 0
    #             a = fastResort(i)
    #             if len(a)>0:
    #                 result['resort'] = a[0]
    #                 result['country'] = a[1]
    print('delta2= ', (datetime.now() - ft).seconds)
    ft = datetime.now()

    return result

def saveCountReq(botName):
    print('добавили запрос')
    arr = getAr(openFile('stati/countOutput.txt').replace("'", '').replace("' ", ''), 0)
    new = True
    for i in arr:
        try:
            if i[0] == botName:
                i[1] += 1
                new = False
                break
        except Exception:
            continue
    if new:
        arr.append([botName, 1])
    writeFile('stati/countOutput.txt', str(arr), 'w')

def checkVisit(name, id, step):
    try:
        arr = getAr(openFile('visits/{0}.txt'.format(name)).replace("'", '').replace("' ", ''), 0)
        ok = True
        new = True
        for i in arr:
            print(i)
            if int(id) == int(i[0]):
                new = False
                d = i[1].replace(' ', '-').replace(':', '-').replace('.', '-').split('-')
                day = datetime(int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4]), int(d[5]))
                dt = (datetime.now() - day).seconds
                i[1] = str(datetime.now()).replace(' ', '-')
                i[2] = 0
                if step == 'vizit':
                    i[2] = 1
                if dt > 15:
                    ok= False
                else:
                    ok= True
        if new:
            print('new visiters')
            arr.append([str(id), str(datetime.now()).replace(' ', '-'), 0])
        writeFile('visits/{0}.txt'.format(name), str(arr).replace(' ', ''), 'w')


    except Exception as er:
        print('frst in ch visits', er)
        writeFile('visits/{0}.txt'.format(name), str([[str(id), str(datetime.now()).replace(' ', '-'), 0]]).replace(' ', ''), 'w')


def butyPeople(user):
    if user['turistcount'] == 1:
        peopleString = 'одного взрослого'
    else:
        peopleString = '{0} взрослых'.format(user['turistcount'])
    childString = ''
    if user['chldold'][0] != '':
        if len(user['chldold']) == 1:
            childString = ' и один ребенок'
        else:
            childString = ' и {0} ребенка'.format(len(user['chldold']))
    resTurists = peopleString + childString
    return resTurists


def chekDepart(text):
    print(text)
    result = []
    te = text.split(' ')
    for j in te:
        if j.lower() == 'омск':
            result.append(1278)
            break

        if j.lower() == 'нск':
            result.append(codCity('Новосибирск'))
            break

        if j.lower() == 'новгород':

            if text[text.index(j) - 1].lower() == 'нижний' or text[text.index(j) - 1].lower() == 'н.' or \
                            text[text.index(j) - 1].lower() == 'н':
                result.append(codCity('Нижний Новгород'))
                break
            if text[text.index(j) - 1].lower() == 'великий':
                result.append(codCity('Великий Новгород'))
                break
    megaT= False
    for i in te:
        if checkCity(i) == 1 and len(i) > 2 and len(result) == 0:
            if codCity(i.capitalize()) != 0:
                try:
                    if te[te.index(i)-1].lower() == 'из':
                        result = [codCity(i.capitalize())]
                        break
                    if te[te.index(i)-1].lower() == 'в':
                        continue
                except Exception:
                    f= 0
                result.append(codCity(i.capitalize()))


    print(result)
    if len(result)==0:
        return 0

    return result[0]

def rassulka():
    import sqlite3
    import vk_api
    vk_session = vk_api.VkApi(
        token='f81089f217939d8d8147041f6393f4ed695d110be9e170f474c07fc36140fe14bbd1b4829557a2f15b13d')
    vk = vk_session.get_api()

    table = sqlite3.connect('data/VKdataBase.db')
    cursor = table.cursor()

    stt = cursor.execute("SELECT *FROM users")
    go = False
    for i in stt:
        if i[-1] == 'ourTourBot':
            print(i[1])
            time.sleep(0.1)

            if i[1] == 486759455:
                go = True

            if go:
                try:
                    mes = 'Вышло обновление Бота для турфирмы!\nПосмотрите краткое видео в этой статье\nhttps://vk.com/@tourbotalisa-obnovlenie-ot-1306'
                    vk.messages.send(user_id=i[1], message=mes)
                    print('ok')
                except Exception:
                    print('not Ok')
                    continue
