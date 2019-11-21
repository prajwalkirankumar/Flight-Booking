import sqlite3
import os
from random import choice

routes = [{"source":"Bengaluru","destination":"Chennai"},
 {"source":"Bengaluru","destination":"Delhi"},
 {"source":"Bengaluru","destination":"Mumbai"},
 {"source":"Bengaluru","destination":"Mangaluru"},
 {"source":"Delhi","destination":"Kolkata"},
 {"source":"Delhi","destination":"Mumbai"},
 {"source":"Delhi","destination":"Chennai"},
 {"source":"Delhi","destination":"Ahmedabad"},
 {"source":"Delhi","destination":"Amritsar"},
 {"source":"Mumbai","destination":"Bengaluru"},
 {"source":"Mumbai","destination":"Chennai"},
 {"source":"Mumbai","destination":"Kolkata"},
 {"source":"Mumbai","destination":"Delhi"},
 {"source":"Mumbai","destination":"Thiruvananthapuram"},
 {"source":"Chennai","destination":"Pondicherry"},
 {"source":"Chennai","destination":"Madurai"},
 {"source":"Chennai","destination":"Kolkata"},
 {"source":"Chennai","destination":"Mumbai"}]



planes = [
 'Air India', 'Air Asia', 'Vistara', 'Indigo', 'Go Air', 'Etihad'
]

times = [
 '10 AM', '12 PM', '2 PM', '4 PM', '6 PM'
]

seats = [
 100, 120, 140, 160, 80, 200, 180, 220
]

coach = [
 'Economy', 'Business', 'First Class'
]

fare = [
 1000, 2000, 3000, 4000, 5000
]


with sqlite3.connect("routes.db") as con:
    con.execute("create table IF NOT EXISTS Routes (id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT NOT NULL, destination TEXT NOT NULL)")
    cur = con.cursor()
    for route in routes:
        cur.execute("INSERT into Routes (source, destination) values (?,?)",(route['source'],route['destination']))
    con.commit()

    con.execute("create table IF NOT EXISTS Flights (id INTEGER PRIMARY KEY AUTOINCREMENT, routeid INTEGER NOT NULL, name TEXT NOT NULL, time TEXT NOT NULL, seats INTEGER NOT NULL, coach TEXT NOT NULL, fare INTEGER NOT NULL)")
    cur = con.cursor()
    loop = 200
    for _ in range(loop):
        for routeid in range(1,19):
            cur.execute("INSERT into Flights (routeid,name,time,seats,coach,fare) values (?,?,?,?,?,?)",(str(routeid), choice(planes),choice(times), str(choice(seats)), choice(coach), str(choice(fare))))
    con.commit()