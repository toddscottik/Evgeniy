# -*- coding: utf-8 -*-
import requests
import sqlite3

conn = sqlite3.connect('databasee.db')
c = conn.cursor()
cor = conn.cursor()
ind = 0

try:
    c.execute(
        '''CREATE TABLE Instituts_API ( Name TEXT UNIQUE, Id INTEGER, Abbr TEXT, indeteficator INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE )''')
except:
    pass

# Функция добавления института
def add_institute(id, name, abbr):
    c.execute("INSERT INTO Instituts_API (Name, Id, Abbr) VALUES ('%s','%d','%s')" % (name, id, abbr))
    conn.commit()

# Функция добавления группы
def add_nameidabbr(id, name, type, level, spec, indet):
    string = "INSERT INTO {ind} ( Id, Name,Type,Level,Spec,Inst_ID) VALUES ('%d','%s','%s','%s','%s','%d')"
    c.execute(string.format(ind="API_" + str(ind)) % (id, name, type, level, spec, indet))
    conn.commit()

# Первая часть - добавление институтов
response = requests.get("http://ruz2.spbstu.ru/api/v1/ruz/faculties").json()

print(response.values())
print(response.keys())
ID = 0
NAME = ""
ABBR = ""
for key in response:
    for key2 in response[key]:
        for keys in key2:
            if keys == "id":
                ID = key2[keys]
                print(ID)
            elif keys == "name":
                NAME = key2[keys]
                print(NAME)
            elif keys == "abbr":
                ABBR = key2[keys]
                print(ABBR)
                add_institute(ID, NAME, ABBR)

# Вторая часть - добавление групп
cor.execute('SELECT * FROM Instituts_API')
row = cor.fetchone()

while row != None:
    q = '''CREATE TABLE {ind}( Id INTEGER PRIMARY KEY, Name TEXT, Type TEXT, Level TEXT, Spec TEXT,  Inst_ID INTEGER NOT NULL,
 FOREIGN KEY (Inst_ID) REFERENCES Instituts_API(Id) )'''
    ind = row[1]
    try:
        c.execute(q.format(ind="API_" + str(ind)))
    except:
        pass

    response = requests.get("http://ruz2.spbstu.ru/api/v1/ruz/faculties/" + str(ind) + "/groups").json()

    print(response.values())
    print(response.keys())
    ID = 0
    NAME = ""
    LEVEL = ""
    TYPE = ""
    SPEC = ""
    for key in response:
        for key2 in response[key]:
            for keys in key2:
                if keys == "id":
                    ID = key2[keys]
                    print(ID)
                elif keys == "name":
                    NAME = key2[keys]
                    print(NAME)
                elif keys == "level":
                    LEVEL = key2[keys]
                    print(LEVEL)
                elif keys == "type":
                    TYPE = key2[keys]
                    print(TYPE)
                elif keys == "spec":
                    SPEC = key2[keys]
                    print(SPEC)
                    try:
                        add_nameidabbr(ID, NAME, TYPE, LEVEL, SPEC, ind)
                    except:
                        pass
    row = cor.fetchone()
    print(row)
c.close()
conn.close()
