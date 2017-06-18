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
                         passwd="rohit8501", local_infile=True, db="RohitDB")
    return db
@app.route('/')
def test1():
    db=db_connect()
    cursor = db.cursor()
    

    file_object = open('R:/data.csv','r')
    reader = csv.reader(file_object)
    row1 = next(reader)
    print reader

    query = "Create table if not exists " + 'QUIZ' + "("
    for i in range(0, len(row1)):
        query += row1[i] + " varchar(30),"

    query += " db_id int unsigned AUTO_INCREMENT PRIMARY KEY );"
    print query
    

    print "Done"
    #return  render_template('R:/check.html')

    db.commit()
    cursor.close()
    return render_template('R:/q6.html')

@app.route('/run',methods=['POST','GET'])
def time500():
    db=db_connect()
    cursor=db.cursor()
    starttime = datetime.datetime.now()
    namee=request.form['gname']

    age1=request.form['age1']
    age2 = request.form['age2']
    print 'ok'
    print "Started 500"
    print namee
    print age1
    print age2
    t = 500

    for i in range(0, t):
        sql="Select count(*)from QUIZ where Age>="+age1+" and Age<="+age2+" and GivenName='"+namee+"'"
        #GivenName='"+namee+"'"
        #sql = "Select Amount from FEED2 where SC_Geography_ID=" + str(op)
        # print sql
        row1=cursor.execute(sql)
    rows=cursor.fetchall()
    print rows
    print row1
    endtime = datetime.datetime.now()
    res = endtime - starttime
    final_result = '500 times : ' + str(res)
    print 'TIME TAKEN FOR 500====',final_result
    return 'TIME TAKEN FOR 500===='+final_result+'Count'+str(rows)

@app.route('/mems',methods=['POST','GET'])
def mems():
    print'Entering memcache'
    db=db_connect()
    cursor=db.cursor()
    namee = request.form['gname']

    age1 = request.form['age1']
    age2 = request.form['age2']
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
                sql = "Select count(*)from QUIZ where Age>=" + age1 + " and Age<=" + age2 + " and GivenName='" + namee + "'"
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
    return result+ rows

if __name__ == '__main__':
    app.run()
