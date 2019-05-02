import sqlite3
import datetime

def clientIsNew(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT botname, login, password FROM client""")
    row = row.fetchall()[1]
    print(row)
    for i in row:
        if(i == login):
            return False
    return True


def getToday():
    realDate = str(datetime.datetime.today())
    flag = 0
    result = ''
    for i in realDate:
        res = 'error'
        if ((i != '-') & (i != ' ') & (i != ':')):
            result = result + i
            year = int(result) * 100000000 + 12000000
        if ((i == ':') & (flag == 1)):  # 2019-04-29 20:01 = 201904292001 in db
            break  # datetime.datetime.today() = 2019-04-29 20:02:14.760226
        if ((i == ':') & (flag == 0)):  # 23 апреля 2019г. в 09:03
            flag = 1
    if (int(result) >= int(year)):
        res = '0'
    else:
        res = '+'

    return {'result': int(result), 'flag': res}

def addClient(botname, login, password, apikey, crm, email, lkcrm, rate, date):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO client VALUES (?,?,?,?,?,?,0,?,?,?)""", (botname, login, password, rate, apikey, crm, email, lkcrm, date))
    print('client added')
    conn.commit()

def getClients():
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()

    row = cursor.execute("""SELECT botname, login, password, rate FROM client""")

    result = []

    for i in row:
        result.append(i)

    return result[0]

def getClientsUsername():
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT login FROM client""")

    result = []

    for i in row:
        result.append(i)

    return result[0][0]

def deleteClient(botname, login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM client WHERE botname = ? AND login = ?""", (botname, login))

def getLimit(botname, login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT date FROM client WHERE botname = ? AND login = ?""", (botname, login))
    row = int(row.fetchall()[0][0])
    realDate = str(datetime.datetime.today())
    flag = 0
    result = ''
    for i in realDate:
        if ((i != '-') & (i != ' ') & (i != ':')):
            result = result + i
        if ((i == ':') & (flag == 1)):                          # 2019-04-29 20:01 = 201904292001 in db
            break                                               # datetime.datetime.today() = 2019-04-29 20:02:14.760226
        if ((i == ':') & (flag == 0)):                          # 23 апреля 2019г. в 09:03
            flag = 1
    realDate = int(result)
    if(row - realDate < 0):
        return -1
    else:
        return row-realDate

def getDate(botname, login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    months = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля', '05': 'мая', '06': 'июня', '07': 'июля',
              '08': 'августа', '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}
    row = cursor.execute("""SELECT date FROM client WHERE botname = ? AND login = ?""", (botname, login))
    row = row.fetchall()[0][0]
    subres = ''
    result = ''
    for i in range(6, 8, 1):
        result = result + row[i]
    for i in range(4, 6, 1):
        subres = subres + row[i]
    subres = months[subres]
    result = result + ' ' + subres + ' '

    for i in range(0, 4, 1):
        result = result + row[i]
    result = result + 'г. в '

    for i in range(8, 10, 1):
        result = result + row[i]
    result = result + ':'
    for i in range(10, 12, 1):
        result = result + row[i]
    return result

def updateClient(botname, login, crm, lkcrm, apikey):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE client SET crm = ?, lkcrm = ?, apikey = ? WHERE botname = ? AND login = ?""", (crm, lkcrm, apikey, botname, login))
    conn.commit()

def updateBalance(botname, login, new):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT balance FROM client WHERE botname = ? AND login = ?""", (botname, login))
    row = int(row.fetchall()[0][0])
    row = row + int(new)
    cursor.execute("""UPDATE client SET balance = ? WHERE botname = ? AND login = ?""", (row, botname, login))
    conn.commit()

def getBalance(botname, login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT balance FROM client WHERE botname = ? AND login = ?""", (botname, login))

    return row.fetchall()[0][0]

def createTables():
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE client
                  (botname text, login text, password text, rate text, apikey text, crm text, balance text, email text, lkcrm text, date text)
                   """)
    print('client table is ready')

# print(getDate('test', 'test'))
# addClient(botname='6929595', login='294940138', password='vafel228' ,apikey='462718ufgd', crm='UonTravel', date='201904292001', lkcrm='hz', email='kustovdanil2@gmail.com', rate='business')