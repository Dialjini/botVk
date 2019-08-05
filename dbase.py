import sqlite3
import datetime


changed = {}

def updateThreadStatus(login, status):
    changed.update([(login, status)])

def timeToStop(login):
    if changed[login]:
        if getBotStatus(login) == 'off':
            return True
    return False


def clientIsNew(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT botname, login, password FROM client""")
    row = row.fetchall()
    for i in row:
        if (i[1] == login):
            return False
    return True

def updateStep(step, username, botname):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()

    cursor.execute("""UPDATE user SET step = ? WHERE username = ? AND botname = ?""",
                   (step, username, botname))
    conn.commit()

def massify(input):
    output = []
    middle = ''
    for i in str(input):
        if i.isdecimal():
            middle = middle + i
        elif(i != '[' or i != ']'):
            if(middle != ''):
                output.append(int(middle))
                middle = ''
            else:
                return output
    return output


def getUserInfo(username, botname):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT username, country, resort, fromcity, date, price, adults,
    children, step, botname, message, nit FROM user WHERE username = ? AND botname = ?""", (username, botname))
    row = row.fetchall()[0]
    result = {'username': row[0], 'country': row[1], 'resort': row[2], 'fromcity': row[3], 'date': row[4],
              'price': int(row[5]), 'adults': int(row[6]), 'children': row[7], 'step': row[8], 'botName': row[9],
              'message': row[10], 'nit': int(row[11])}
    if(result['children'][0] == '['):
        print(result)
        result['children'] = massify(input=result['children'])
    return result


def addUser(username, country, resort, fromcity, date, price, adults, children, step, botname, nit):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO user VALUES (?,?,?,?,?,?,?,?,?,?,0,?)""",
                   (username, country, resort, fromcity, date, price, adults,
                    children, step, botname, nit))
    conn.commit()


def addNewUser(username, login):
        conn = sqlite3.connect("vk.db")
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO user VALUES (?,0,0,0,0,0,0,0,'frstwaitrespons',?,0,0)""", (username, login))
        conn.commit()
        print('New User')

def getStep(username):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()

    row = cursor.execute("""SELECT step FROM user WHERE username = ?""", (username,))

    return row.fetchall()[0][0]

def userUpdate(value, userid, collum, botname):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()

    cursor.execute("""UPDATE user SET ? = ? WHERE username = ? AND botname = ?""",
                   (collum, value, userid, botname))
    conn.commit()


def fullUserUpdate(user, username):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    print('========================================')
    print(user)
    print('========================================')
    cursor.execute("""UPDATE user SET country = ?, resort = ?, fromcity = ?, date = ?, price = ?, adults = ?,
    children = ?, step = ?, nit = ? WHERE username = ? AND botname = ?""",
                   (str(user['country']), str(user['resort']), str(user['fromcity']), str(user['date']), str(user['price']), str(user['adults']), str(user['children']), str(user['step']), str(user['nit']), str(username), str(user['botName'])))
    conn.commit()

def deleteUser(username, botname):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM user WHERE username = ? AND botname = ?""", (username, botname))
    conn.commit()
    print('User ' + str(username) + ' was deleted.')


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
    cursor.execute("""INSERT INTO client VALUES (?,?,?,?,?,?,0,?,?,?,0)""",
                   (botname, login, password, rate, apikey, crm, email, lkcrm, date))
    print('client added')
    conn.commit()


def getToken(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()

    row = cursor.execute("""SELECT password FROM client WHERE login = ?""", (login,))

    return row.fetchall()[0][0]


def getClients():
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()

    row = cursor.execute("""SELECT botname, login, password, rate FROM client""")

    result = []

    for i in row:
        result.append(i)

    return result[0]


def getBotname(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT botname FROM client WHERE login = ?""", (login,))
    return row.fetchall()[0][0]


def getClientsUsername():
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT login FROM client""")

    result = []

    for i in row:
        result.append(i)

    return result


def getBalance(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT balance FROM client WHERE login = ?""", (login,))
    return row.fetchall()[0][0]


def deleteClient(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM client WHERE login = ?""", (login,))
    conn.commit()
    print('User ' + str(login) + ' was deleted.')


def getLimit(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT date FROM client WHERE login = ?""", (login,))
    row = int(row.fetchall()[0][0])
    realDate = str(datetime.datetime.today())
    flag = 0
    result = ''
    for i in realDate:
        if ((i != '-') & (i != ' ') & (i != ':')):
            result = result + i
        if ((i == ':') & (flag == 1)):  # 2019-04-29 20:01 = 201904292001 in db
            break  # datetime.datetime.today() = 2019-04-29 20:02:14.760226
        if ((i == ':') & (flag == 0)):  # 23 апреля 2019г. в 09:03
            flag = 1
    realDate = int(result)
    if (row - realDate < 0):
        return -1
    else:
        return row - realDate


def addPass(password, login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE client SET password = ? WHERE login = ?""", (password, login))
    conn.commit()


def getDate(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    months = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля', '05': 'мая', '06': 'июня', '07': 'июля',
              '08': 'августа', '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}
    row = cursor.execute("""SELECT date FROM client WHERE login = ?""", (login,))
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


def updateClient(login, crm, lkcrm, apikey, botname):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE client SET botname = ?, crm = ?, lkcrm = ?, apikey = ? WHERE login = ?""",
                   (botname, crm, lkcrm, apikey, login))
    conn.commit()


def updateRate(login, rate):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE client SET rate = ? WHERE login = ?""",
                   (rate, login))
    conn.commit()


def updateBalance(login, new):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT balance FROM client WHERE login = ?""", (login,))
    row = int(row.fetchall()[0][0])
    row = row + int(new)
    cursor.execute("""UPDATE client SET balance = ? WHERE login = ?""", (row, login))
    conn.commit()


def getFields(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT crm, lkcrm, apikey balance FROM client WHERE login = ?""", (login,))

    return row.fetchall()[0]


def getRate(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT rate FROM client WHERE login = ?""", (login,))

    return row.fetchall()[0][0]


def lastMesUpdate(login, message):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE user SET message = ? WHERE username = ?""", (message, login))
    conn.commit()


def createTables():
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS client
                  (botname text, login text, password text, rate text, apikey text, crm text, balance text, email text, lkcrm text, date text, botactive text)
                   """)
    print('client table is ready')

    cursor.execute("""CREATE TABLE IF NOT EXISTS user
                   (username text ,country text, resort text, fromcity text, date text, price text, adults text, children text,
                   step text, botname text, message text, nit text)
                   """)
    print('user table is ready')
    conn.commit()

def getClientContacts(name):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()

    row = cursor.execute("""SELECT password, crm, login, email, botname FROM client WHERE login = ?""", (name, ))
    row = row.fetchall()
    result = {'apikey': '', 'domain': '', 'idVk': '', 'email': '', 'botname': ''}
    try:
        result['apikey'] = row[0][0]
        result['domain'] = row[0][1]
        result['idVk'] = row[0][2]
        result['email'] = row[0][3]
        result['botname'] = row[0][4]
        return result
    except Exception as er:
        print('err line 298 in dbase ({0})'.format(er))
        return {}

def getActiveUsers():
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT login FROM client WHERE botactive = ?""", ('on',))

    result = []

    for i in row:
        result.append(i)

    return result


def upBot(login, botstatus):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE client SET botactive = ? WHERE login = ?""", (botstatus, login))
    conn.commit()


def getBotStatus(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT botactive FROM client WHERE login = ?""", (login,))

    return row.fetchall()[0][0]


def getPass(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT password FROM client WHERE login = ?""", (login,))

    return row.fetchall()[0][0]

def getUsers(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    row = cursor.execute("""SELECT username, step, message FROM user WHERE botname = ?""", (login, ))
    return row.fetchall()

def delUsers(login):
    conn = sqlite3.connect("vk.db")
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM user WHERE botname = ?""", (login,))
    conn.commit()
    print('Users successfully deleted')

createTables()
# print(getClients())
# deleteClient(180547049)
# addClient(botname='6929595', login='294940138', password='no' ,apikey='462718ufgd', crm='UonTravel', date='201904292001', lkcrm='hz', email='kustovdanil2@gmail.com', rate='business')
# deleteUser(294940138)
# print(getUsers(login='180547049'))
print(getUserInfo(username='294940138', botname='180547049'))
# print('STEP NOW: '+getStep('294940138'))
# delUsers(login='180547049')


