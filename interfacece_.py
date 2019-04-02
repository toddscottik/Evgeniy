# http://ruz2.spbstu.ru/api/v1/ruz/faculties/
# -*- coding: utf-8 -*-
import sqlite3
import requests

ind = ""
op = 0
f = False

conn = sqlite3.connect('databasee.db')
c = conn.cursor()
cor = conn.cursor()

# Вывод списка часов по предметам для определённой группы
def tlist():
    b = "SELECT * FROM {namt}"
    c.execute(b.format(namt="GROUP_" + p))
    row = c.fetchone()
    summLec = 0
    summPra = 0
    summLab = 0
    print("Количество часов: ")
    while row != None:
        summLec = summLec + row[2]
        summPra = summPra + row[3]
        summLab = summLab + row[4]
        print("Name: " + row[1] + " | " + "Часов лекций: " + str(row[2]) + " | " + "Часов практик: " + str(
            row[3]) + " | " + "Часов лабораторных: " + str(row[4]) + "\n")
        row = c.fetchone()
    print("-----------------------------------------------------------")
    print("Лекций: " + str(summLec) + "| Практик: " + str(summPra) + "| Лабораторных: " + str(
        summLab) + "| Всего: " + str(summLec + summPra + summLab))


# Функция добавления нового предмета в таблицу
def add_lesson(namelesson, nam):
    b = "INSERT INTO {namt} (name,Group_ID) VALUES('%s','%d') "
    c.execute(b.format(namt="GROUP_" + p) % (namelesson, ind))
    conn.commit()


# Функция прибавления чаоов к лекциям
def increment_lec(nemelesson, numhours, nam):
    b = "UPDATE {namt} SET hoursofLec = (hoursofLec + ?) WHERE name = ?"
    p = NUMe[:5] + '_' + NUMe[6:]
    c.execute(b.format(namt="GROUP_" + p), (numhours, nemelesson))
    conn.commit()


# Функция прибавления чаоов к практикам
def increment_pra(nemelesson, numhours, nam):
    b = "UPDATE {namt} SET hoursofPra = hoursofPra + ? WHERE name = ?"
    c.execute(b.format(namt="GROUP_" + nam), (numhours, nemelesson))
    conn.commit()


# Функция прибавления чаоов к лабораторным
def increment_lab(nemelesson, numhours, nam):
    b = "UPDATE {namt} SET hoursofLab = (hoursofLab + ?) WHERE name = ?"
    c.execute(b.format(namt="GROUP_" + nam), (numhours, nemelesson))
    conn.commit()


# Вывод списка институтов
cor.execute('SELECT * FROM Instituts_API')
row = cor.fetchone()
print(row)
while row is not None:
    print(str(row[3]) + ")" + str(row[2]))
    row = cor.fetchone()

NUM = input("Выберите институт: ")

c.execute('SELECT * FROM Instituts_API WHERE indeteficator=?', (NUM))
row = c.fetchone()
instID = row[1]
# Ввод номера группы
NUMe = input("Выберите группу: ")
q = '''SELECT * FROM {ind} WHERE Name = {nom}'''
ind = row[1]

NUMet = "'" + NUMe + "'"

iino = "API_" + str(ind)

try:
    c.execute(q.format(ind=iino, nom=NUMet))
except:
    pass
idi = c.fetchone()[0]

p = NUMe[:5] + '_' + NUMe[6:]
bf = '''CREATE TABLE {numy} ( `ID` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, `name` TEXT UNIQUE, `hoursofLec` 
                                INTEGER DEFAULT 0, `hoursofPra` INTEGER DEFAULT 0, `hoursofLab` INTEGER DEFAULT 0, Group_ID INTEGER NOT NULL,
 FOREIGN KEY (Group_ID) REFERENCES API_''' + str(ind) + '''(Id)  )'''
try:
    c.execute(bf.format(numy="GROUP_" + p))
except:
    f = True
if f != True:
    global i
    # noinspection PyRedeclaration
    i = 0
    f = -1
    month_thone = {1, 3, 5, 7, 8, 10, 12}
    month_thzero = {4, 6, 9, 11}
    month_feb = {2}
    date_day = 3
    date_month = 9
    while date_month != 13:
        date_day = date_day + 7
        print(date_day)
        print(date_month)
        if date_month in month_thone:
            if date_day > 31:
                date_day = date_day - 31
                date_month = date_month + 1
        elif date_month in month_thzero:
            if date_day > 30:
                date_day = date_day - 30
                date_month = date_month + 1
        elif date_month in month_feb:
            if date_day > 28:
                date_day = date_day - 28
                date_month = date_month + 1
        response = requests.get(
            "http://ruz2.spbstu.ru/api/v1/ruz/scheduler/" + str(idi) + "?date=2018-" + str(date_month) + "-" + str(
                date_day))
        print(response)
        response = response.json()
        for key in response:
            if key == "week":
                i = i + 1
                print(key)
                for keys in response[key]:
                    print("response[", key, "][", keys, "]= ", response[key][keys])
            elif key == "days":
                f = f + 1
                while f != 1000:
                    # noinspection PyBroadException
                    u = False
                    try:
                        if response[key][f]:
                            u = True
                    except:
                        break
                    if u:
                        for keys in response[key][f]:
                            if keys != "lessons":
                                print("response[", key, "][", f, "][", keys, "]= ", response[key][f][keys])
                            if keys == 'lessons':
                                for kes in response[key][f][keys]:
                                    # print("Response[", key, "][", f, "][", keys, "][", kes, "]=", response[key][f][keys])
                                    for j in kes:
                                        if j != "typeObj" and j != "auditories" and j != "groups":
                                            print("        Lessons[", j, "]=", kes[j])
                                            if j == "subject":
                                                nameoflesson = kes[j]
                                            try:
                                                add_lesson(nameoflesson, p)
                                            except:
                                                pass
                                            if j == "additional_info":
                                                if kes[j] != "" and kes[j] != "Поток":
                                                    op = 1
                                                    print("\\" + kes[j] + "|")
                                                else:
                                                    print("-")

                                        elif j == "typeObj":
                                            for b in kes[j]:
                                                #                                         print("                Lessons[", j, "][", b, "]=", kes[j][b])
                                                inc = 2
                                                if kes[j][b] == 14:
                                                    increment_lec(nameoflesson, inc, p)
                                                    print("Podschital LECTSII " + nameoflesson)
                                                if kes[j][b] == 27:
                                                    if op == 1:
                                                        inc = 1
                                                        op = 0
                                                    else:
                                                        inc = 2
                                                    increment_pra(nameoflesson, inc, p)
                                                    print("Podschital PRACTIKU " + nameoflesson)
                                                    inc = 2
                                                if kes[j][b] == 26:
                                                    if op == 1:
                                                        increment_lab(nameoflesson, inc / 2, p)
                                                        op = 0
                                                    else:
                                                        increment_lab(nameoflesson, inc, p)
                                                    print("Podschital LABU " + nameoflesson)

                        f = f + 1
                f = -1
tlist()
c.close()
conn.close()
