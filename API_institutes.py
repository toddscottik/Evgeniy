# -*- coding: utf-8 -*-
import bs4
import requests
import urllib
import csv
import sqlite3

conn = sqlite3.connect('databasee.db')
c = conn.cursor()

try:
    c.execute('''CREATE TABLE Instituts_API ( Name TEXT UNIQUE, Id INTEGER, Abbr TEXT, indeteficator INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE )''')
except:
    pass

def add_nameidabbr(id,name,abbr):
    c.execute("INSERT INTO Instituts_API (Name, Id, Abbr) VALUES ('%s','%d','%s')" % (name,id,abbr))
    conn.commit()

response = requests.get("http://ruz2.spbstu.ru/api/v1/ruz/faculties").json()

print (response.values())
print (response.keys())
ID=0
NAME =""
ABBR=""
for key in response:
    for key2 in response[key]:
        for keys in key2:
            if keys == "id":
                ID=key2[keys]
                print(ID)
            elif keys == "name":
                NAME = key2[keys]
                print(NAME)
            elif keys == "abbr":
                ABBR = key2[keys]
                print(ABBR)
                add_nameidabbr(ID,NAME,ABBR)
c.close()
conn.close()
