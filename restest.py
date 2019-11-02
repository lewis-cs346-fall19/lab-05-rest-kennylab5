#!/usr/bin/python3

import cgi
import cgitb
import os
import json
import passwords
import MySQLdb
cgitb.enable()

conn = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER,
                       passwd = passwords.SQL_PASS, db = "fishes")
cursor = conn.cursor()
cursor.execute("USE fishes;")

form = cgi.FieldStorage()

def hello():     
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()

    print("""<!DOCTYPE html>
    <html>
    <head>
        <title>restest</title>
    </head>
    <body>
        <h1>use /restest.py/fish</h1>
    </body>
    </html>""")

def yellow():     
    print("Status: 302 Redirect")
    print("Location: /cgi-bin/restest.py/boi")
    print()

def jsona():
    print("Content-Type: application/json")
    print("Status: 200 OK")
    print()
    x = {'hello':'how','are':'you'}
    x_json = json.dumps(x)
    print(x_json)

def sql():
    cursor.execute("SELECT * FROM fish;")
    print("Content-Type: application/json")
    print("Status: 200 OK")
    print()

    strangs = cursor.fetchall()
    for row in strangs:
        myid = row[0]
        mytype = row[1]
        mysize = row[2]
        myeat = row[3]
        if myeat > 0:
            eat = 'true'
        else:
            eat = 'false'
        x = {'id':myid,'type':mytype,'size':mysize,'edible':eat}
        x_json = json.dumps(x)
        print(x_json)

def specialsql():
    numb = path[6:]
    cursor.execute("SELECT * FROM fish WHERE id LIKE %s;", numb)
    print("Content-Type: application/json")
    print("Status: 200 OK")
    print()

    strangs = cursor.fetchall()
    for row in strangs:
        myid = row[0]
        mytype = row[1]
        mysize = row[2]
        myeat = row[3]
        if myeat > 0:
            eat = 'true'
        else:
            eat = 'false'
        x = {'id':myid,'type':mytype,'size':mysize,'edible':eat}
        x_json = json.dumps(x)
        print(x_json)

def postsql():
    myid = form["id"].value
    mytype = form["type"].value
    mysize = form["size"].value
    myeat = form["size"].value
    cursor.execute("INSERT INTO fish (type, size, eat) VALUES (%s, %s, %s)", (mytype,mysize,myeat))
    new_id = cursor.lastrowid
    print("Status: 302 Redirect")
    print("Location: /cgi-bin/restest.py/fish/{}".format(new_id))
    print()
    

path=os.environ['PATH_INFO']
if path == '/boi':
    hello()
elif path == '/jsona':
    jsona()
elif path == '/fish':
    if os.environ['REQUEST_METHOD'] == 'GET':
        sql()
    elif os.environ['REQUEST_METHOD'] == 'POST':
        postsql()
    else:
        yellow()
elif len(path) > 5:
    if path[0:5] == '/fish':
        specialsql()
else:
    yellow()
