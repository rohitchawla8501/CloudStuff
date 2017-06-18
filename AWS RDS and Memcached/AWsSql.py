from flask import Flask
from flask import Flask, render_template, redirect, url_for, request,make_response
import os
import memcache

import csv
import warnings
import datetime

import pymysql
import random
app = Flask(__name__)
warnings.filterwarnings("ignore")
def db_connect():
    db = pymysql.connect(host="", port=3306, user="",
                         passwd="", local_infile=True, db="RohitDB")
    return db



@app.route('/')
def test1():
    db=db_connect()
    cursor = db.cursor()
 
    #cursor.execute("LOAD DATA INFILE 'R:/FeedGrains.csv' INTO TABLE FEED IGNORE 1 LINES")

    #cursor.execute("LOAD DATA LOCAL INFILE 'R:/FeedGrains.csv' INTO TABLE FEED4 FIELDS TERMINATED BY ',' ;")
    #csv_data = csv.DictReader(file('R:/FeedGrain.csv'))

    #for row in csv_data:
        #print ''
        #cursor.execute('INSERT INTO FEED(SC_Group) VALUES("%s")',row['SC_Group_ID'])

        #print row['SC_Group_ID']
        #[rn]
    
    file_object = open('R:/FeedGrains.csv','r')
    reader = csv.reader(file_object)
    row1 = next(reader)
    print reader

    query = "Create table if not exists " + 'FEED4' + "("
    for i in range(0, len(row1)):
        query += row1[i] + " varchar(30),"

    query += " db_id int unsigned AUTO_INCREMENT PRIMARY KEY )"
    print query
    cursor.execute(query)
   

    print "Done"
    return  render_template('R:/check.html')

    db.commit()
    cursor.close()

@app.route('/500queries',methods=['POST','GET'])
def time500():
    db=db_connect()
    cursor=db.cursor()
    starttime = datetime.datetime.now()

    print 'ok'
    print "Started 500"
    t = 500
    for i in range(0, t):
        op = random.randint(1, 250)
        sql = "Select Amount from FEED2 where SC_Geography_ID=" + str(op)
        # print sql
        cursor.execute(sql)
    endtime = datetime.datetime.now()
    res = endtime - starttime
    final_result = '500 times : ' + str(res)
    print 'TIME TAKEN FOR 500====',final_result
    return '500 Done'


@app.route('/1000queries',methods=['POST','GET'])
def time1000():
    db=db_connect()
    cursor=db.cursor()
    starttime = datetime.datetime.now()

    print 'ok'
    print "Started 500"
    t = 1000
    for i in range(0, t):
        op = random.randint(1, 250)
        sql = "Select Amount from FEED2 where SC_Geography_ID=" + str(op)
        # print sql
        cursor.execute(sql)
    endtime = datetime.datetime.now()
    res = endtime - starttime
    final_result = '1000 times : ' + str(res)
    print 'TIME TAKEN FOR 1000====',final_result
    return '1000 Done'
@app.route('/2500queries',methods=['POST','GET'])
def time2500():
    db=db_connect()
    cursor=db.cursor()
    starttime = datetime.datetime.now()

    print 'ok'
    print "Started 500"
    t = 2500
    for i in range(0, t):
        op = random.randint(1, 250)
        sql = "Select Amount from FEED2 where SC_Geography_ID=" + str(op)
        # print sql
        cursor.execute(sql)
    endtime = datetime.datetime.now()
    res = endtime - starttime
    final_result = '2500 times : ' + str(res)
    print 'TIME TAKEN FOR 2500====',final_result
    return '2500 Done'
@app.route('/mems',methods=['POST','GET'])
def mems():
    print'Entering memcache'
    db=db_connect()
    cursor=db.cursor()
    t=500

    memc = memcache.Client([''], debug=1)
    #memc.set('hello', 'world')
    c=memc.get('hello')
    x = 0
    #start = time.time()
    starttime = datetime.datetime.now()
    #for i in range(1, 500):
    random_query = memc.get('got_query')
    print ('Random Query',random_query)
    if not random_query:
            for i in range(0, t):
                op = random.randint(1, 250)
                sql = "Select Amount from FEED2 where SC_Geography_ID=" + str(op)
                # print sql
                cursor.execute(sql)
            rows = cursor.fetchall()
            memc.set('got_query', rows, 500)
            #flask.flash("updated memcached with MySQL data")
    else:
            if (x == 0):
                print("Loaded data from memcached")
                x = 1
    #end = time.time()
    endtime = datetime.datetime.now()
    res = endtime - starttime
    print res
    result=str(res)
    return res


if __name__ == '__main__':
    app.run()
