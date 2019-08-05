from lxml import etree
from zeep import Client, xsd

from datetime import  date, timedelta, time
import time
import fnck
import  requests
import  json




def hotelInformation(id):
    client = Client(
        wsdl='https://module.sletat.ru/XmlGate.svc?singleWSDL',

    )
    login = 'legionne@gmail.com'
    password = 'ZauD76s91Ha'

    result = client.service.GetHotelInformation(hotelId= id , _soapheaders={'AuthInfo': {'Login': login, 'Password': password}})
    print(result)




def getTours(ctFrom, country, hotel, Mants, Mints, ppls, dat, kids, kidAd, resort, minPri, crV= 'RUB'):

    client = Client(
            wsdl='https://module.sletat.ru/XmlGate.svc?singlewsdl'
            # wsdl= 'XmlGate.xml'

        )
    # print(dir(client.service))
        # client.wsdl.dump()
    res = []
    hot = []
    print('resort://', resort)

    res = []
    resort = str(resort)

    for i in resort.split('/'):
        if int(i) > 0:
            res.append(int(i))

    if hotel==0:
        hot=[]
    else:
        hot = [hotel]

    tDat = dat.split('/')


    if len(tDat) == 1:
        delta = timedelta(days=4)
        dat = str(dat).replace('.',' ').split()
        datPl = date(int(dat[2]),int(dat[1]),int(dat[0])) + delta
        datMn = date(int(dat[2]), int(dat[1]), int(dat[0])) - delta
        datPl = str(datPl).replace('-',' ').split()
        datPl = datPl[2] + '.' + datPl[1]+'.' + datPl[0]
        datMn = str(datMn).replace('-', ' ').split()
        datMn = datMn[2] + '.' + datMn[1]+'.' + datMn[0]
    else:
        delta = timedelta(days=0)
        if tDat[0] < tDat[1]:
            mdat = str(tDat[0]).replace('.', ' ').split()
            mmdat = str(tDat[1]).replace('.', ' ').split()
        else:
            mdat = str(tDat[1]).replace('.', ' ').split()
            mmdat = str(tDat[0]).replace('.', ' ').split()
        datPl = date(int(mmdat[2]), int(mmdat[1]), int(mmdat[0]))
        datMn = date(int(mdat[2]), int(mdat[1]), int(mdat[0]))
        datPl = str(datPl).replace('-', ' ').split()
        datPl = datPl[2] + '.' + datPl[1] + '.' + datPl[0]
        datMn = str(datMn).replace('-', ' ').split()
        datMn = datMn[2] + '.' + datMn[1] + '.' + datMn[0]



    print(datMn)
    print(datPl)
    print(country)
    print(ctFrom)
    print(ppls)
    print(Mints)
    print(Mants)
    login = 'legionne@gmail.com'
    password = 'Ud8SWzh6Wk9'

    # crV = 'BYN'

    cod= client.service.CreateRequest(countryId=country, cityFromId=ctFrom, hotels=hot, cities=res, adults=ppls, nightsMin=Mints, nightsMax = Mants, departFrom=datMn, departTo=datPl,currencyAlias= crV, hotelIsNotInStop=True, hasTickets=True, ticketsIncluded=True, useTree=False, includeDescriptions=False, showEconomOnly=True, kids=kids, kidsAges=kidAd, priceMin= minPri, _soapheaders={'AuthInfo': {'Login': login, 'Password': password}})
    print('cod request:{0}'.format(str(cod)))
    while 1:
        c=0
        time.sleep(5)
        otv1=client.service.GetRequestState(requestId=cod,_soapheaders={'AuthInfo': {'Login': login, 'Password': password}} )

        for o in otv1:
            if o['IsProcessed']==True:
                # print(o)
                c+=1
        if c==len(otv1):
            break




    #print(cod)
    # time.sleep(30)
    otv=client.service.GetRequestResult(requestId=cod,_soapheaders={'AuthInfo': {'Login': login, 'Password': password}} )

    # print(otv)
    tours=[]
    # print(otv)
    tours=otv['Rows']['XmlTourRecord']
    # tours = otv
    # print(tours[0],tours[1],tours[2])
    # print(tours)


    return tours
    # return otv



def jsonGetTours(ctFrom, country, hotel, Mants, Mints, ppls, dat, kids, kidAd, resort, minPri):
    res = []
    hot = []
    res = []
    resort = str(resort)
    if int(resort) == 0:
        res = []
    else:
        for i in resort.split('/'):
            res.append(int(i))
    if hotel == 0:
        hot = []
    else:
        hot = [hotel]

    tDat = dat.split('/')

    if len(tDat) == 1:
        delta = timedelta(days=4)
        dat = str(dat).replace('.', ' ').split()
        datPl = date(int(dat[2]), int(dat[1]), int(dat[0])) + delta
        datMn = date(int(dat[2]), int(dat[1]), int(dat[0])) - delta
        datPl = str(datPl).replace('-', ' ').split()
        datPl = datPl[2] + '.' + datPl[1] + '.' + datPl[0]
        datMn = str(datMn).replace('-', ' ').split()
        datMn = datMn[2] + '.' + datMn[1] + '.' + datMn[0]
    else:
        delta = timedelta(days=0)
        mdat = str(tDat[0]).replace('.', ' ').split()
        mmdat = str(tDat[1]).replace('.', ' ').split()
        datPl = date(int(mmdat[2]), int(mmdat[1]), int(mmdat[0]))
        datMn = date(int(mdat[2]), int(mdat[1]), int(mdat[0]))
        datPl = str(datPl).replace('-', ' ').split()
        datPl = datPl[2] + '.' + datPl[1] + '.' + datPl[0]
        datMn = str(datMn).replace('-', ' ').split()
        datMn = datMn[2] + '.' + datMn[1] + '.' + datMn[0]


    login = 'legionne@gmail.com'
    password = 'ZauD76s91Ha'

    # cod = client.service.CreateRequest(countryId=country, cityFromId=ctFrom, hotels=hot, cities=res, adults=ppls,
    #                                    nightsMin=Mints, nightsMax=Mants, departFrom=datMn, departTo=datPl,
    #                                    hotelIsNotInStop=True, hasTickets=True, ticketsIncluded=True, useTree=False,
    #                                    includeDescriptions=False, showEconomOnly=True, kids=kids, kidsAges=kidAd,
    #                                    priceMin=minPri,
    #                                    _soapheaders={'AuthInfo': {'Login': login, 'Password': password}})
    # print('cod request:{0}'.format(str(cod)))

    f = requests.get('https://module.sletat.ru/Main.svc/GetTours?login={0}&password={1}&countryId={2}&cityFromId={3}&hotels={4}&cities={5}&adults={6}&nightsMin=Mints{7}&nightsMax={8}&departFrom={9}&departTo={10}&hotelIsNotInStop=1&hasTickets=1&ticketsIncluded=1&useTree=0&includeDescriptions=False&showEconomOnly=1&kids={11}&kidsAges={12}&priceMin=13'.format(login, password, country, ctFrom, hot, res, ppls, Mints, Mants, datMn, datPl, kids, kidAd, minPri))
    idR = f.text
    print(int(idR))


# print(getTours(fnck.codCity('Киев'), fnck.codCountry('Египет'), 0, 10, 9,2,'07.07.2018',0,[],0, 0))
#print((getTours(fnck.codCity('Новосибирск'),  fnck.codCountry('Турция'), 0, 18, 12,2,'10.08.2019/15.08.2019',0,[],0, 0)))
# jsonGetTours(fnck.codCity('Новосибирск'), 113, 0, 8, 8,2,'21.06.2018',0,[],0, 200000)


# hotelInformation(78825)
