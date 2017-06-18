#Name: Vikas Chandrashekar
#id  : 1001248880
#term: Summer 2016
#Assignment_2 

import flask, flask.views
from random import randint
import os
import functools
import urlparse
from pymongo import MongoClient
import json
import ast 
import time
from bson import json_util
from bson.json_util import dumps
import numpy as np
import plotly
from sklearn.cluster import KMeans
from sklearn.feature_extraction import FeatureHasher
app = flask.Flask(__name__)

# Don't do this!
app.secret_key = "bacon"
users = {'vikas':'vikas'}
class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')
    
    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('index'))
        required = ['username', 'passwd']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('index'))
        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        if username in users and users[username] == passwd:
            flask.session['username'] = username
        else:
            flask.flash("Username doesn't exist or incorrect password")
        return flask.redirect(flask.url_for('index'))

def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("A login is required to see the page!")
            return flask.redirect(flask.url_for('index'))
    return wrapper

class Remote(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('remote.html')
        
    @login_required
    def post(self):
        clusters = flask.request.form['e3']
        #nn.ec2.internal
        MONGODB_HOST = 'localhost'
        MONGODB_PORT = 27017
        DBS_NAME = 'cloudplat'
        COLLECTION_NAME = 'quiz'
#x=raw_input("Enter column1 name")
#y=raw_input("Enter column2 name")
        FIELDS = {'b': True, 'd': True, '_id': False}

        connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
        collection = connection[DBS_NAME][COLLECTION_NAME]
        projects = collection.find(projection=FIELDS)
        json_projects = []

        x=[]
        y=[]
        for project in projects:
            conv=ast.literal_eval(json.dumps(project))
            json_projects.append(conv)
    
        for d in json_projects:
            a = d['b']
            b = d['d']
            x = [float(a), float(b)]
            y.append(x)
        connection.close()
        X = np.array(y)
        starttime = time.time()
	flask.flash(clusters)
        kmeans = KMeans(n_clusters=int(clusters))
        kmeans.fit(X)
        centroids = kmeans.cluster_centers_
        labels = kmeans.labels_
        xcen = []
        ycen = []
	flask.flash(xcen)
        for i in range(len(centroids)):
            xcen.append(centroids[i][0])
            ycen.append(centroids[i][1])
        endtime = time.time() - starttime 
        global maxcluster
        maxcluster = 0
        xgrp = [[],[],[],[],[],[],[],[],[],[]]
        ygrp = [[],[],[],[],[],[],[],[],[],[]]
        i = 0
        for k in json_projects:
            m = d['b']
            n = d['d']
            try:
                xgrp[labels[i]].append(float(m))
                ygrp[labels[i]].append(float(n))
                i += 1
                if (maxcluster < int(labels[i])):
                        maxcluster = int(labels[i])
            except:
                continue

        mydata = []
        for i in range(maxcluster+1):

                    mydata.append(dict(
                                       x=xgrp[i],
                                       y=ygrp[i],
                                       type='scatter',
                                       mode='markers',

                                       ),)

        mydata.append(dict(
                           x=xcen,
                           y=ycen,
                           type='scatter',
                           mode='markers'
                           ),)
        flask.flash(mydata)
	
        graphs = [
                  dict(
                       data= mydata,
                       layout=dict(
                                   title='Scatter graph'
                                   )
                       )
                  ]

        ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
        graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
        return flask.redirect(flask.url_for('remote'))
        
    
app.add_url_rule('/',
                 view_func=Main.as_view('index'),
                 methods=["GET", "POST"])
app.add_url_rule('/remote/',
                 view_func=Remote.as_view('remote'),
                 methods=['GET', 'POST'])


app.debug = True
app.run()
