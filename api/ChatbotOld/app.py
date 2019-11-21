import wikipedia,os
from flask import Flask
from flask import request,jsonify

import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append('/Users/prajwalkirankumar/Documents/WT2/api/Chatbot/')

from chatbot import Chat,reflections,multiFunctionCall
from flask_sse import sse
from apscheduler.schedulers.background import BackgroundScheduler
import random
app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

from flask_cors import CORS

CORS(app)
def getFlightDetails(string, sessionID = "general"):
    flightToReturn = []
    string = string[0:len(string)-1]
    cur = con.cursor() 
    cur.execute("SELECT * from FLIGHTS where id = (?)", (string,))
    res = cur.fetchall()
    # for key in flights.keys():
    #     if key == string:
    #         temp = convertToList(flights[key])
    #         flightToReturn.append(temp)

    # print(tabulate([l for l in flightToReturn], headers=["Source", "Destination", "Departure", "Arrival", "Company", "FLight Number"]))
    return str(res)

def returnFlights(string, sessionID = "general"):
    string = string.split(',')
    source = string[0].split(' ')[1]
    source = source.capitalize()
    destination = string[1].split(' ')[0]
    destination = destination.capitalize()
    cur = con.cursor() 
    cur.execute("SELECT id FROM routes WHERE source = (?) AND destination = (?)", (source, destination))
    routeid = cur.fetchall()
    routeid = routeid[0][0]
    print(routeid)

    cur.execute("SELECT * FROM flights WHERE routeid = (?)", (str(routeid),))
    res = cur.fetchall()
    # #each id will be mapped to source, destination, dep_time, arr_time and company

    # flightsToReturn = []
    # for key in flights.keys():
    #     if flights[key].source == source and flights[key].destination == destination:
    #         temp = convertToList(flights[key])
    #         flightsToReturn.append(temp)

    # print(tabulate([l for l in flightsToReturn], headers=["Source", "Destination", "Departure", "Arrival", "Company", "FLight Number"]))
    return str(res)
    # flightsToReturnString = "Source\t\tDestination\tDeparture\tArrival\tCompany\tFLight Number\n"

    # for l in flightsToReturn:
    #     tempstr = ""
    #     for ele in l:
    #         tempstr += ele
    #         tempstr += "\t"
    #     tempstr += "\n"
    #     flightsToReturnString += tempstr
    # return flightsToReturnString


def showSeats(fno, sessionID="general"):
    fno = fno[0:len(fno)-1]
    cur = con.cursor() 
    cur.execute("SELECT seats from FLIGHTS where id = (?)", (fno,))
    seats = cur.fetchall()
    # for key in flights.keys():
    #     if key == fno:
    #         for sno in flights[key].seats.keys():
    #             if flights[key].seats[sno].booked == 0:
    #                 print("Seat Number: ", sno, " Seat Type: ", flights[key].seats[sno].type)

    return str(seats[0][0])

def bookFlight(string, sessionID="general"):
    fno = string.split(',')[0]
    sno = string.split(',')[1]
    sno = sno[0:len(sno)-1]
    # fno = fno[0:len(fno)-1]
    cur = con.cursor() 
    cur.execute("SELECT seats FROM flights WHERE id = (?)", (fno,))
    seats = cur.fetchall()
    print(seats[0][0])

    cur.execute("UPDATE flights SET seats = seats - (?) WHERE id = (?)",(sno, fno))
    
    cur.execute("SELECT seats FROM flights WHERE id = (?)", (fno,))
    seats = cur.fetchall()
    
    # for key in flights.keys():
    #     if key == fno:
    #         if(flights[key].seats[sno].booked == 0):
    #             flights[key].seats[sno].booked = 1
    #             print("Succesfully booked")
    #         else:
    #             print("This seat has already been taken")
    return str(seats[0][0])

call = multiFunctionCall({"showSeats":showSeats,
        "returnFlights":returnFlights, 
        "getFlightDetails":getFlightDetails,
        "bookFlight":bookFlight})
chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)),"examples/flightRules.template"), reflections,call=call)
chat.converse_http("Hi","") 

@app.route('/chat', methods = ["POST"])
def hello():
    print(request.json)
    message = request.json['message']
    print(message)                         
    return chat.converse_http(message),200

    
def whoIs(query,sessionID="general"):
    try:
        return wikipedia.summary(query)
    except:
        for newquery in wikipedia.search(query):
            try:
                return wikipedia.summary(newquery)
            except:
                pass
    return "I don't know about "+query
   
@app.route('/chat/<message>')
def hello(message):
	return jsonify("HELLO"+message),200


def send_message():
    with app.app_context():
        sse.publish({"Offers": "25% Offer!","Paytm":"20% Offer!","GPAY":"20% Offer!","BookMyShow":"20% Offer!"}, type='greeting')
        return "Message sent!",200

def get_schd_time():
    return random.randrange(5,20)

sched = BackgroundScheduler(daemon=True)
sched.add_job(send_message,'interval',seconds=get_schd_time())
sched.start()
# conn = None

import sqlite3

@app.route('/db')
def db():
    
    conn = sqlite3.connect('database.db')
    for i in range(0,4):
        cur = conn.cursor()
        cur.execute("SELECT * FROM students LIMIT 5 OFFSET "+str(i*5))
        print(cur.fetchall())

    conn.close()
    return "SUCC",200

con = sqlite3.connect("routes.db",check_same_thread=False)

@app.route('/getSources',methods=["GET"])
def listSources():
    cur = con.cursor()
    sources = cur.execute('SELECT distinct source from Routes').fetchall()
    return jsonify(sources),200

@app.route('/getDestinations/<source>')
def listDest(source):
    cur = con.cursor()
    destinations = cur.execute('SELECT distinct destination from Routes where source="{}"'.format(source)).fetchall()
    return jsonify(destinations),200

@app.route('/getFlights/<routeid>/<offset>')
def listFlights(routeid,offset):
    cur = con.cursor()
    cur.execute("SELECT * from flights where routeid={} LIMIT 5 OFFSET {}".format(routeid, offset))
    return jsonify(cur.fetchall()),200
   
@app.route('/getAllFlights/<source>/<destination>/<offset>')
def listAllFlights(source,destination,offset):
    cur = con.cursor()
    print(source)
    print(destination)
    routeid = cur.execute("SELECT id from Routes where source=(?) AND destination=(?)",(source,destination)).fetchall()[0][0]
    print(routeid)
    cur.execute("SELECT * from flights where routeid=(?) LIMIT 5 OFFSET (?)",(str(routeid), str(offset)))
    return jsonify(cur.fetchall()),200
   


if __name__ == '__main__':
    conn = sqlite3.connect('database.db')
    conn.execute('DROP TABLE students')
    print("Opened database successfully")
    conn.execute('CREATE TABLE students (id NUMBER PRIMARY KEY,name TEXT, addr TEXT, city TEXT, pin TEXT)')
    print("Table created successfully")

    cur = conn.cursor()
    for i in range(20):
        cur.execute("INSERT INTO students (id,name,addr,city,pin) VALUES ("+str(i)+",'PKK','ADDR','BLR',122)")
    conn.commit()
    conn.close()
    app.debug = True
    app.run()


