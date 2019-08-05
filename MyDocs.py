# мои документы CRM
import requests
import json
import fnck
import const

keys = {
    'ourTourBot':'8GN370r681h9SdCpCDl5jm3xa9LAs908Bcpp2w5cj9Nb7Mt3G4UKs9j198B56gxF',
    'RoRo':'hF0f6Cki7oZaWeX54ce5O4bO32Nb36nE6qKufwARS6187SZ51e0948XxIIZb7bD4',
    'hunty_muntu':'M78w83LFENWe3YyLGP457357Ft9d2p2fJ6o8088b7266GVS9UBGi0O3be8I1K07k',
    'pltrv': 'ng8qVgoC2kMqeK2UO8jGHhrJq81xc5cx3a99WrwG9A6Odfv8qvNI9Uf6F3A9612i',
    'suntorini': 'XlI1o9wUDqP77fVYU2ZLf9gEM03T7w6y2r9aV5x373C041h4X2KV32GhiiLci3s3',
    'tvoymir': 'W9kVicUUr76gK6To4Q5u9u7kJUwnl1XT984ER6UQ605lirD61k27B7z4wrhlcVBb',
    'premiumtour': '34I9bODgOEahqWRel6Ufqju1ws86WL1210kZ29Iwx48EfX0MO4ACTTpKs66d7xoy',
    'agentcharkina': 'ND04q523J7901asHSQ06RVaod5xN48y9932D4SJv2xbEIradoXtgiCmSAdgG7c0p',
    'vesmirtur': '9m904113072DNFR05pE4lehagZ2poV2A4c6Ekmf0Cu9gXhJQEju03xhmrsn78U25',
    'palma86': '8fp6AtX32ES02j5Im85qpU2qbrInJ1LKqnV7lw8eQ4q9Q4B5U9wJ3XXQJ9ci4CXQ',
    'marseltur':'phRQ6k4AC8JW45pQTuKqoEL00dYzo5N3FeHL8L8C9V5rhh1L74O4NsR8PEM7T8XW',
    'clubcocolocotour': 'Sogvr0uHhMZQ2llwOOvCSS482XkzV5Y480c0L0NjiQBLuUFkoCM4St38LgC640a5',
    'pegas_72': '4HAPH6CB2W1Hzr5UCG8ii6mDYVoPxggI0Mk56X7EKaxopcqgFtVcBA4dk1LGh6U6',
    'sputnik35': 'igaHT2qQ5vB1NCkWgM4m9h20anU0C152d79X6fzDq4BhnsKPst578QIQ3Q0uAYy7',
    'belka_tur': 'pgbGGY9G7gr5pnzilj52KiDAa4AODDg8Ae9Hm18om915Pm33H31MAB7oxUp5dHY6',
    'samara': 'v9Yxo0Y0089kXOh7b26N0CwkbadWI6xQXlSkD155iC4qn266ldRRqMcBOtSF7iAj',
    'zefir72': 'u6302lumqMrZciOF6lcrf66eMv0sXYLBmT9swyRaN3rV9V4gT3ieER7rzM7QkGeC',
    'miosun': 'Y6aM1320V4DLDY3z2QYYvdfISmX37VP3A3iEt215Cn2kZ2S63c929VFqrdhd11t6',
    'aquatur' :'vugap2YJFI8Bg9dQx31Cm127mQL99chnR5wY7G9DFuRS2723kc37Ngor6Qp0xm9F',
    'dinar': '9O6BKT3O0MPXYEQ1iMCSwr76UyAYvUuOW4QA1Ddjf8RyVH19V7iSjGxZg9k814N4',
    'provence670611':'S1i950q4oKj43O0K617GCsQdY3N2Mx8fuk7uPojm3a8d6P94i0X5RNTQYtup22V4',
    'tyzemec_kazan': 'lPB0I5dKmSed2s1N1A5BsQci5wBe8cC3B11nQRXu21CVE8cgJf071Gb15M2gZh4V',
    'sinapelsin': 'ID16zvxDuYdDZUBqbqNZrt217dPpRN6MSNJcPkDwPcBn55GSIfi3FBSE9qx5XIb8',
    'apelsinorai': '5s3xRZLwbI89su4B7jiQI6sks8kjvqbg3Yo5CWJ08CCzQ6vE1E63qxEhvtKhn7Mr',
    'travel4u': 'bAuKgp792wuMhwzjIY642S2fP2GPeRLx32O0qYbi9nxoxx4qsSJlYnALcq7D9u4f',
    'tourism163': 'idzG0IIZbb379ls0R2kV2uSM7ZF0hjzZ81nn0U18tEHb58l4L8wwsX5ekII33W08',
    'putevki_travel': 'mWE7oWlyJ7lg0326qGNm4qr1qar03b9f9xh0Yk87W73SUlBv256JuF2ZcaxBcYW9',
    'turyizulyanovska': '6n72S8Ba7F3jfqVe8mv73D8O7L4FQ2evVH4O6of3yJxy9FSS1Jzm05Zd2icg91k6',
    'hott_nsk': 'O6y9S49Fc7XX4JLiZo1uP8vZsn4BC1l6w797410vhM3H94QFnMdbiFBvpw1s4E0s',
    'lechu_kh': 'pkf92Q1ZxicJhZDBF37UvurKxJZQ3958vcFOJ87quyi85lz456Z9dM9f6kMIK77G',
    'surgot': 'Dwgo51xTj81nA4cQ7a39t5rIR9Fzj03j3MY1HG8b50j6vvRdH57nHZNgb875JmAF',
    'belojarskiy': 'FbYIGB941Pomi94Ee3tRS8weKNzvT99zkQBX53G9AjwKUkk2febEeqj6DkQRb8iW',
    'fortunachelny': 'dh3DVhuxr1cw7hz7XkcB0ACwaIwOCp50qPtMOX1n3UTS70B2Jpc51vF8Y6us2Y63',
    'yarsletat': '3lF7QBZ2Ewjt7uJc7Bjn8b7iHl2E36ygfIgcW5ww04rukRj7I5R8SbU9A7SCVAwL',
    'fiveseson': 'Zgf66ivwb6nLVs8GZ3Pq39IbkY1IOLnrL6k54LV4547Jkoyvr9192qwauNq472eT',
    'boleuh': 'sVDZqN20izWUWjTKxAS500GcNGL2tpf7mvuF9Ue6TBB0gkU1zA4vYpu6FCLfka3P',
    'visatravel72': '7crV7r7taESpI8PSyg8N4pUTc3qAzk07h6h3o0x5l0NxK4Y9XjNcY46e20apA671',
    'kyrortymira': 'W182s86XCi1xHjK96Zboz424Vcl9TG7gB9G9Z07YzwLQnh6cyhID5zN4thl9J0fy',
    'georgievtravel': 'J1TKqlIiZA26PgIjQl2RwHrqF1ElOJhC358mOTk51nfVeZo1hsxL6yuR6i4J7Au3',
    'otpusk_turexpert': 'aIvLR8yU9xG9mnlH4r7akNZcdoJCTDcqc0B0f3t0Q9PC4tqGsOAU6qe26IER0v74',
    'tvoy_mir_spb': 'o50rituQwdGhOber7pz7r2OVobvUgorAL0i63hY3GBtA2mvSNiQfmnj4636y1z0l',
    'tour_yarmarka': 'JxSPF4Leitw9EjuCn3960HNmC5vQQ6r79YKp2S4X2N1uiupP43UopEAb4z94R6CG',
    'happyholidayclub': '5IMWnk32KtqPikmk4Vlzc157fmXVKBLuhCgfi7CCJzqfRov1liEF9siUEKdsd50A',
    'zagranica71': 'zsHH94i5aerL74485fo57P65678ILU6hs4ng0RAwPKtjLEpziaz65cwUyb3Vb791',
    'abakantur': 'e5543cs0D6PV4obCv6A0NYhh5AyR47Ic9642Qc87Vgv22LgGTDzjG72B54Yy4Y8T',
    'aktiv_vidnoe': 'X87AblJi7Zs30XrvMr4l7IEOFcnZqDufMPE0WNvHh45U9D7s1QRq5u1MpOMX4h0o',
    'tury.travel': 'cY1PNJ6t05W9yI743Zx8G0KrWb11o3eIT2eewkJ5Fpdn1gkwkETc0dy1yo5l1N31',
    'geograftourkaluga': 'FfHBRdXF5t5OkWNQ2ip1dJFhYUrgmV2iZrv2vphb0BmA77FwHiC5SUu9yA3sauaf',
    'clubtuibutovo': 'FJSWXRhjjfvGj2PN4945a7h4wxT8oX37yp2KFq51JXvf4K5nBC2k1uMX4A5h3jaZ',
    'threeaccs': 'afW2CPTpIm2q35LuHTEhCm64pwuM3f307Ro8uCJV5MkNLClomupE3aC2E7rtppBE',
    'arkhangelsktur': '7GI0H11995Xz4AaB148K8msS10X6X3N4KSkoJ1v836O5omK7i19YPW32Auh63Lh5',
    'sletat_ru_93': '1g77Q6m7nV4wqnYW1RxwZEd72Y5w13f10iRsmqgJO3n38kwr87CTjSz0t88ivVo4',
    'romantik': 'S1huk5OxvR2Jwgfalki1K46lz6BXMpd4SkpA3aicpMlEyb4zKtlR4c7Zn5tRJzbd'
}

accs = {
    'ourTourBot': 'mdt708',
    'belka-tur': 'belka-tur',
    'samara': 'tyrmarket',
    'zefir72': 'Zefir72',
    'miosun': 'mio',
    'aquatur': 'aquatur',
    'dinar': 'geografiaufa',
    'provence670611': 'provans',
    'tyzemec_kazan': 'tuzemec',
    'sinapelsin': 'sinapelsin',
    'apelsinorai': 'apelsinorai',
    'travel4u': 'travel4u',
    'tourism163': 'kalinatrvl',
    'putevki_travel': 'putevki-travel',
    'turyizulyanovska': '1001tur-ulyanovsk',
    'hott_nsk': 'slon-best',
    'lechu_kh': 'lechu-kh',
    'surgot': 'surgutintur',
    'belojarskiy': 'belojar-mgp',
    'fortunachelny': 'fortuna-chelny',
    'yarsletat': 'tour-centr',
    'fiveseson': '5thseason',
    'boleuh': 'boleuh',
    'visatravel72': 'visatum',
    'kyrortymira': 'kurort-mira',
    'georgievtravel': 'smartpe',
    'otpusk_turexpert': 'tur-expert',
    'tour_yarmarka': 'yarmarkaturov',
    'tvoy_mir_spb': 'tvoy-mir',
    'happyholidayclub': 'happyholiday',
    'zagranica71': 'zagranica71',
    'abakantur': 'misuk',
    'aktiv_vidnoe': 'aktiv',
    'tury.travel': 'voyage-msk',
    'geograftourkaluga': 'ultra-tour',
    'clubtuibutovo': 'countravel',
    'threeaccs': 'legian-tur',
    'arkhangelsktur': 'nordwest29',
    'sletat_ru_93': 'l-travel',
    'romantik': 'romantik-tur'

}

managest = {
    'samara': [3],
    'dinar': [13]
}


def make_request(data, metod, client, con):
    url = 'https://{0}.moidokumenti.ru/api/{1}'.format(con['domain'] ,metod)

    res = requests.post(url, data=data)
    print()
    # print(json.loads(res.text))
    result = json.loads(res.text)
    print('--------req', metod, result)
    return result


def objId(obj, inputC, client, con):
    param = json.dumps({})
    data = {'params': param, 'key': con['apikey']}
    countries = make_request(data=data, metod='get-{0}-list'.format(obj), client=client, con= con)
    print(countries)
    for c in countries['data']:
        if c['title'].lower() == inputC.lower():
            id_c = c['id']
    return id_c


def addReq(user, discr, client, cont):
    print('add MyDocs', client, cont)
    print(len(user['chldold']), user['chldren'])
    if user['chldold'] == ['']:
        user['chldold'] = []

    try:
        country = objId(obj='country', inputC= fnck.nameCountry(user['country']),client= client, con= cont)
        deprt = objId(obj='departure', inputC= fnck.nameCity(user['fromcity']), client= client, con= cont)
    except Exception as er:
        country = 0
        deprt = 0
        print('add errore')
        print(er)
    turist_id = addTurist(user, client, cont)
    discr = discr + '\n' + fnck.nameTown(user['resort']) +'\n' + fnck.nameHotel(user['hotel'])
    print(user)
    print(user['date'])
    datAee = user['date'].split('.')
    try:
        dataMy = '{0}-{1}-{2}'.format(datAee[2], datAee[1], datAee[0])
    except Exception:
        dataMy = '20-02-2019'
    param = json.dumps({'tourist_type': 'tourist_temp', 'tourist_id': turist_id, 'country_id1': country,
                        'flightdate_from': dataMy,
                        'flightdate_to': dataMy, 'persons': user['adults'], 'children': len(user['children']), 'children_ages': user['children'],'nights_from': user['nit'], 'nights_to': user['nit'],
                        'comment': discr, 'departure_id1': deprt, 'price_to': user['price'] if user['price'] !=0 else 1})
    data = {'params': param, 'key': cont['apikey']}

    return_data = make_request(data=data, metod='create-preorder', client= client, con= cont)
    print(return_data)

    manList = getManagerList(client)['data']
    push(user, client, [i['id'] for i in manList], con= cont)
    for m in manList:
        try:
            if m['email'] != '':
                pushMail(text= discr.replace('\n', '<br>'), client= client, email= m['email'], to= m['name'], id= return_data['preorder_id'], con=cont)
        except Exception as er:
            print(er)


def push(user, client, ids, con):
    url = 'https://{0}.moidokumenti.ru/api/send-push'.format(con['domain'])
    manId = managest[client] if client in managest else [33]
    data = {'params': json.dumps({'manager_ids': ids, 'title': 'Новая заявка', 'text': 'Заявка из Vk bot', 'url': 'https://{0}.moidokumenti.ru/'.format(accs[client])}),
            'key': con['apykey']}
    res = requests.post(url, data=data)
    print()
    print(json.loads(res.text))

def pushMail(text, client, email, to, id, con):
    url = 'https://{0}.moidokumenti.ru/api/send-email'.format(accs[client])
    text = const.text4muD.format(to, id) + text
    manId = managest[client] if client in managest else [33]
    data = {'params': json.dumps({'for_name': to, 'for_email': email, 'from_name': 'bot', 'from_email': 'no-reply@moidokumenti.ru', 'title': 'Новая заявка', 'text': text,
                                  'url': 'https://{0}.moidokumenti.ru/'.format(con['domain'])}),
            'key': con['apikey']}
    res = requests.post(url, data=data)
    print()
    print(json.loads(res.text))

def getManagerList(client, con):
    url = 'https://{0}.moidokumenti.ru/api/get-manager-list'.format(con['domain'])
    data = {'params': json.dumps({'count': 100, 'fields': ['id', 'name', 'email'], 'offset': 0}),
            'key': con['apikey']}
    res = requests.post(url, data=data)
    print()
    return json.loads(res.text)

def addTurist(user, client, con):
    print('tur')
    try:
        manId = managest[client][0]
    except Exception:
        manId = 3
    param = json.dumps(
        {'name': '{0} {1}'.format(user['first_name'], user['last_name']), 'tel': user['phone'], 'email': '--', 'tags': 'Заявка из Inst бота',
         'manager_id': manId,
         'office_id': 1})
    data = {'params': param, 'key': con['apikey']}

    turist = make_request(data=data, metod='add-tourist-temp', client= client)
    if turist['result'] == 'success':
        return turist['tourist_temp_id']
    else:
        return 'error'



if __name__ != '__main__':
    param = json.dumps({'count': 10, 'offset': 0, 'fields': ['id', 'name']})
    # data = {'params': param,
    #         'key': keys['samara']}
    # data = {'params': param, 'key': keys['dinar']}
    # for i in make_request(data= data, metod='get-manager-list', client= 'dinar', {})['data']:
    #
    #     print(i)